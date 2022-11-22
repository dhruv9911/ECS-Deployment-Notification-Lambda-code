import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # TODO implement
    print(event)
    ecs_client = boto3.client("ecs")
    print(event["detail"]["eventName"])
    
    if event["detail"]["eventName"] == "SERVICE_DEPLOYMENT_COMPLETED" :
	    serviceName = event["resources"][0].split("/")[-1]
	    print("ServiceName :"+ serviceName)
	    deployedServiceId = event["detail"]["deploymentId"]
	    print(deployedServiceId)
	    #clusters = ecs_client.list_clusters()
	    #print(clusters)
	    clusterName = "Sample"
	    response = ecs_client.describe_services(cluster=clusterName, services=[serviceName])
	    print(response)
	    #ecsClusterArn = response["services"][0]["clusterArn"]
          ecsClusterArn = "arn:aws:ecs:us-east-1:086429042168:cluster/Sample"
	    ecsContainerName = response["services"][0]["loadBalancers"][0]["containerName"]
	    #ecsTaskId = response["services"][0]["taskDefinition"]
	    ecsDeploymenIds = response["services"][0]["deployments"]
	    print(len(ecsDeploymenIds))
	    deps = 0
	    for deps in range(len(ecsDeploymenIds)):
	    	if ecsDeploymenIds[deps]["id"] == deployedServiceId:
	    		print("true")
	    		ecsTaskId = ecsDeploymenIds[deps]["taskDefinition"]
	    		desiredCount = ecsDeploymenIds[deps]["desiredCount"]
	    		pendingCount = ecsDeploymenIds[deps]["pendingCount"]
	    		runningCount = ecsDeploymenIds[deps]["runningCount"]
	    		failedTasks = ecsDeploymenIds[deps]["failedTasks"]
	    		createdAt = ecsDeploymenIds[deps]["createdAt"]
	    		updatedAt = ecsDeploymenIds[deps]["updatedAt"]
	    		launchType = ecsDeploymenIds[deps]["launchType"]
	    		
	    		#print("ecsTaskId : " +ecsTaskId)
	    		#print("desiredCount : ",desiredCount)
	    		#print("pendingCount : ",pendingCount)
	    		#print("runningCount : ",runningCount)
	    		#print("failedTasks : ",failedTasks)
	    		#print("createdAt : ", createdAt.strftime('%m/%d/%Y::%I'))
	    		#print("updatedAt : ", updatedAt)
	    		#print("launchType : "+ launchType)
	    		body_text1 = "Account ::     086429042168<br>Service-Name :: " + serviceName + "<br>EcsTaskId ::   " + ecsTaskId
	    		body_text = "<br>Created On ::   " + createdAt.strftime('%m/%d/%Y::%I') + "<br>Launch Type ::  " + launchType
	    		deps = deps + 1
	    		print("ecsClusterArn :" + ecsClusterArn)
	    		print("ecsContainerName :" + ecsContainerName)
	    		print("ecsTaskId : "+ ecsTaskId)
	    		#print("ecstaskSetArn : "+ ecstaskSetArn)
	    		sendEmail(body_text1, body_text, serviceName)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
        
    }
    
def sendEmail(body_text1, body_text, serviceName):

	SENDER = "notification@dhruvsingh.live"
	RECIPIENT = ['dhruv@dhruvsingh.live', 'dhruv@dhruvsingh.live']
	AWS_REGION = "us-east-1"
	# Specify a configuration set. If you do not want to use a configuration
	# set, comment the following variable, and the 
	# ConfigurationSetName=CONFIGURATION_SET argument below.
	CONFIGURATION_SET = "ConfigSet"
	# The subject line for the email.
	SUBJECT = "ECS deployment notification for Service : " + serviceName + " : in Dev/UAT/Prod environment"
	# The email body for recipients with non-HTML email clients.
	BODY_TEXT = ("Please find the details about the Service.\r\n"
	             "Environment --> 086429042168 \r\n"
	             +body_text1 + body_text
	            )
	            
	# The HTML body of the email.
	BODY_HTML = """<html>
	<head></head>
	<body>
	  <h3>ECS Service Deployment completed in 086429042168.</h3>
	  <p>Please find following details ... 
	  </p>
	  <br>{body_text1}{body_text}</p><br>
	</body>
	</html>
	            """.format(body_text1=body_text1, body_text=body_text)          

	CHARSET = "UTF-8"
	client = boto3.client('ses',region_name=AWS_REGION)
	
	# Try to send the email.
	try:
	    #Provide the contents of the email.
	    response = client.send_email(
	        Destination={
	            'ToAddresses': RECIPIENT,
	        },
	        Message={
	            'Body': {
	                'Html': {
	                    'Charset': CHARSET,
	                    'Data': BODY_HTML,
	                },
	                'Text': {
	                    'Charset': CHARSET,
	                    'Data': BODY_TEXT,
	                },
	            },
	            'Subject': {
	                'Charset': CHARSET,
	                'Data': SUBJECT,
	            },
	        },
	        Source=SENDER,
	        # If you are not using a configuration set, comment or delete the
	        # following line
	        #ConfigurationSetName=CONFIGURATION_SET,
	    )
	# Display an error if something goes wrong.	
	except ClientError as e:
	    print(e.response['Error']['Message'])
	else:
	    print("Email sent! Message ID:"),
	    print(response['MessageId'])

