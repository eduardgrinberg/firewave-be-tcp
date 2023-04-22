import boto3


class Notifier:
    def __init__(self):
        self.topic_arn = 'arn:aws:sns:eu-central-1:442017065919:firewave-poc-sns'
        self.sns_client = boto3.client('sns')

    def notify(self):
        # Create a client object for SNS

        # Publish a message to the SNS topic
        response = self.sns_client.publish(
            TopicArn=self.topic_arn,
            Message='Hello, world!'
        )

        # Print the response to confirm that the message was published successfully
        print(response)
