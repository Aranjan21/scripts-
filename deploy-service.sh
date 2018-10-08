service=$1
version=$2
names=$3

if [ $# != 3 ];  then
    echo "Usage : sh deploy-service.sh <service name> <version> <elb-target-group-name>"
    exit 0
fi

arn=$(aws elbv2 describe-target-groups --names "${names}" --query TargetGroups[].TargetGroupArn --profile elb --region us-east-2 --output text)
instances=$(aws elbv2 describe-target-health  --target-group-arn "${arn}" --query TargetHealthDescriptions[].Target.Id --profile elb --region us-east-2 --output text)

ip=$(ifconfig | awk '/inet addr/{print substr($2,6)}' | grep -E '172.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')

echo Instance Private IP Address is: ${ip}


for instanceid in $instances; do

    instanceip=$(aws ec2 describe-instances --instance-ids ${instanceid} --query Reservations[].Instances[].PrivateIpAddress --profile elb --region us-east-2 --output text)
    instancename=$(aws ec2 describe-tags --filters Name=resource-id,Values="${instanceid}" Name=key,Values=Name --query Tags[].Value --profile elb --region us-east-2 --output text)

    if [ $instanceip = $ip ]
    then
        echo "Found ${instancename} with IP ${ip}"
        echo "Removing ${instancename} from Target Group"

        aws elbv2 deregister-targets --target-group-arn "${arn}" --targets Id=${instanceid} --profile elb --region us-east-2
        echo "Waiting for traffic to drain. wait 60 seconds"
        sleep 60

        echo "Deploy Started"
        rm -rf $service-$version.tar

        wget https://s3.us-east-2.amazonaws.com/lunera-images/$service-$version.tar

        echo $version > version.txt

        sudo mkdir -p /lunera/code/$service

        sudo mkdir -p /lunera/data/$service

        sudo chown -R lundaemons.lundaemons /lunera/code/$service

        sudo chown -R lundaemons.lundaemons /lunera/data/$service

        sudo tar xvf $service-$version.tar -C /lunera/code/$service

        sudo mv version.txt /lunera/code/$service/$service-$version

        cd /lunera/code/$service

        sudo systemctl stop $service

        sudo rm current

        sudo ln -s $service-$version current

        sudo chown -R lundaemons.lundaemons /lunera/code/$service

        sudo rm -f /etc/systemd/system/$service.service

        sudo mkdir -p /usr/local/lib/systemd/system

        sudo cp -f /lunera/code/$service/current/systemd/$service.service /usr/local/lib/systemd/system

        sudo systemctl daemon-reload
        sudo systemctl start $service
        sudo systemctl enable $service
        #sudo systemctl status $1

        #journalctl -u $service -f

        sleep 5

        #killall journalctl
        echo "Deploy Ended"

        echo "Adding ${instancename} back to Target Group"
        aws elbv2 register-targets --target-group-arn "${arn}" --targets Id=${instanceid} --profile elb --region us-east-2

    fi
done

echo "All done"
