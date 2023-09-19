import subprocess
import tabulate


containers_data = subprocess.check_output("docker ps", shell=True).decode("utf-8").split("\n")[1:-1]

output = []

for container in containers_data:
    filtered_data = list(filter(lambda x: x, container.split("  ")))
    output.append([filtered_data[0], *filtered_data[3:]])

print(tabulate.tabulate(output, headers=["CONTAINER ID", "CREATED", "STATUS", "PORTS", "NAMES"]))
