import certstream
import time

output_file = "domains.txt"
count = 0  # Counter to track processed domains
start_time = time.time()  # Track script start time
RUN_TIME = 60  # Script will run for 60 seconds

def callback(message, context):
    global count
    if time.time() - start_time > RUN_TIME:
        print("Time limit reached. Exiting...")
        exit(0)  # Terminate script after 60 seconds

    if message['message_type'] == "certificate_update":
        domains = message['data']['leaf_cert']['all_domains']
        with open(output_file, "a") as f:
            for domain in domains:
                if not domain.startswith("*"):  # Ignore wildcards
                    count += 1
                    if count % 5 == 0:  # Only save every 5th domain
                        print(f"Saving: {domain}")
                        f.write(domain + "\n")

certstream.listen_for_events(callback, url='wss://certstream.calidog.io/')
