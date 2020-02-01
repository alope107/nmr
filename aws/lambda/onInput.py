import json
import urllib.parse
import boto3
from time import gmtime, strftime

print('Loading function')

batch_client = boto3.client('batch')
RESULT_PREFIX = "results"

def lambda_handler(event, context):
    print("Got called!!!")
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    start_job(bucket, key)
    

def job_name(prefix, t=None):
    if not t:
        t = gmtime()
    return prefix + strftime("%d_%b_%Y_%H-%M-%S", t)
    
def get_file_id(key):
    slash_loc = key.rindex("/")
    dot_loc = key.rindex(".")
    return key[slash_loc + 1:dot_loc]
    
def start_job(bucket, key):
    uri = "s3://" + bucket + "/" + key
    name = job_name("from_lambda_")
    s3_prefix = bucket + "/" + RESULT_PREFIX
    file_id = get_file_id(key)
    print("Input " + uri)
    print("File ID: " + file_id)
    print("Job name: " + name)
    print("Results to go to: " + s3_prefix)
    # resp = batch_client.submit_job(
    #     jobName=name,
    #     jobQueue='Hello-Docker-Queue',
    #     jobDefinition='Malice-real:2',
    #     containerOverrides={
    #         'vcpus': 2,
    #         'memory': 1024,
    #         'command': [
    #             uri,
    #             "--phase1_islands", "2",
    #             "--phase1_generations", "10",
    #             "--phase1_evo_rounds", "1",
    #             "--phase2_islands", "2", 
    #             "--phase2_generations", "10",
    #             "--phase2_evo_rounds", "1",
    #             "--least_squares_max_iter", "10",
    #             "--mcmc_walks", "10", 
    #             "--mcmc_steps", "20",
    #             "--s3_prefix", s3_prefix,
    #             "--output_dir", file_id],
    #     },
    #     retryStrategy={
    #         'attempts': 1
    #     },
    #     timeout={
    #         'attemptDurationSeconds': 600
    #     }
    # )
    resp = batch_client.submit_job(
        jobName=name,
        jobQueue='Hello-Docker-Queue',
        jobDefinition='Malice-real:2',
        containerOverrides={
            'vcpus': 15,
            'memory': 8192,
            'command': [
                uri,
                "--num_threads", "10",
                "--s3_prefix", s3_prefix,
                "--output_dir", file_id],
        },
        retryStrategy={
            'attempts': 1
        },
        timeout={
            'attemptDurationSeconds': 60*60*5
        }
    )