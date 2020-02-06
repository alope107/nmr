from complexLambda.onFailedJob import lambda_handler

def integration_test():
    event = {
        'version': '0', 
        'id': 'ad9cd466-3333-a6ed-01c5-5c5e7050aa9c', 
        'detail-type': 'Batch Job State Change', 
        'source': 'aws.batch', 
        'account': '549329392535', 
        'time': '2020-02-05T22:25:57Z', 
        'region': 'us-west-2', 
        'resources': ['arn:aws:batch:us-west-2:549329392535:job/aed495ba-8ce3-4330-8c4f-f587529e43ab'], 
        'detail': {
            'jobName': 'from_lambda_05_Feb_2020_17-24-56', 
            'jobId': 'aed495ba-8ce3-4330-8c4f-f587529e43ab', 
            'jobQueue': 'arn:aws:batch:us-west-2:549329392535:job-queue/Hello-Docker-Queue', 
            'status': 'FAILED', 
            'attempts': [
                {
                    'container': {
                        'containerInstanceArn': 'arn:aws:ecs:us-west-2:549329392535:container-instance/dbf8b129-7059-43dd-bdcf-19822de57d4b', 
                        'taskArn': 'arn:aws:ecs:us-west-2:549329392535:task/cea1a5c3-3840-4ec9-9096-f808142a204c', 
                        'exitCode': 0, 
                        'logStreamName': 'Malice-real/default/cea1a5c3-3840-4ec9-9096-f808142a204c', 
                        'networkInterfaces': []
                    }, 
                    'startedAt': 1580935755961, 
                    'stoppedAt': 1580941556637, 
                    'statusReason': 'Essential container in task exited'
                }
            ], 
            'statusReason': 'Essential container in task exited', 
            'createdAt': 1580923496516, 
            'retryStrategy': {'attempts': 1}, 
            'startedAt': 1580935755961, 
            'stoppedAt': 1580941556637, 
            'dependsOn': [], 
            'jobDefinition': 'arn:aws:batch:us-west-2:549329392535:job-definition/Malice-real:2', 
            'parameters': {}, 
            'container': {
                'image': 'redcliffesalaman/malice', 
                'vcpus': 15, 
                'memory': 8192, 
                'command': [
                    's3://malice/input/10Ucmt7mSJozR1g86B_AcvVGbadLR_DaJ.csv', 
                    '--num_threads', '10', 
                    '--s3_prefix', 'malice/results', 
                    '--output_dir', '10Ucmt7mSJozR1g86B_AcvVGbadLR_DaJ'
                ], 
                'jobRoleArn': 'arn:aws:iam::549329392535:role/ContainerRole', 
                'volumes': [], 
                'environment': [], 
                'mountPoints': [], 
                'ulimits': [], 
                'exitCode': 0, 
                'containerInstanceArn': 'arn:aws:ecs:us-west-2:549329392535:container-instance/dbf8b129-7059-43dd-bdcf-19822de57d4b', 
                'taskArn': 'arn:aws:ecs:us-west-2:549329392535:task/cea1a5c3-3840-4ec9-9096-f808142a204c', 
                'logStreamName': 'Malice-real/default/cea1a5c3-3840-4ec9-9096-f808142a204c', 
                'networkInterfaces': [], 
                'resourceRequirements': []}, 
                'timeout': {
                    'attemptDurationSeconds': 18000
                }
            }
        }
    lambda_handler(event, None)

if __name__ == "__main__":
    integration_test()