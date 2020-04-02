from locust import HttpLocust, TaskSet, task, between
import random
import json
import urllib.parse

class WebsiteTasks(TaskSet):
    def on_start(self):
        with open('dev-v2.0.json', 'r') as myfile:
            data=myfile.read()

        obj = json.loads(data)

        self.questions = []
        for doc in obj['data']:
            for paragraph in doc['paragraphs']:
                for qobj in paragraph['qas']:
                    #print(f"###{qobj['question']}\n\n")
                    self.questions.append(qobj['question'])

    @task
    def about(self):
        response = self.client.get('api/search?query=' + urllib.parse.quote(random.choice(self.questions)), headers={"User-Agent":"locust"})
        print(response.content)


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    wait_time = between(5, 15)
