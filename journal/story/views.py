from django.shortcuts import render
from .models import Entry
from django.contrib.auth.decorators import login_required
import os
import datetime
import json
# api
from rest_framework import status
from .serializers import EntrySerializer
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Entry
import random


# @login_required
def home(request):
    entries = Entry.objects.all().order_by("-date_start")
    entries = entries.values()

    # show pictures when in local host and turning on it manually
    def show_pictures():
        if os.getenv('SHOW_PICTURES') == "True" and os.getenv('PICTURE_CONFIG') != "":
            # fake db that has pictures sorted by year and date
            pictures_config = os.getenv('PICTURE_CONFIG')
            with open(pictures_config) as data_file:
                picture_data = json.load(data_file)
            picture_day_limit: int = 12  # how many pics show a day

            # don't need to crete new array because .update updates entry in memory
            for entry in entries:
                date_start = entry['date_start']
                date_end = entry['date_end']
                date_range = [datetime.date.fromordinal(ordinal) for ordinal in range(date_start.toordinal(), date_end.toordinal())] # arr that has start to end date
                all_pics_found = []
                for curr_date in date_range: # can do singe and day and multiple day picture for a day because use array for loop
                    curr_year = str(curr_date.year)
                    curr_date = str(curr_date)

                    # validate that pictures exist for that day
                    # adding random pictures for each day with max limit and adding them to final array that is entry has
                    if picture_data.get(curr_year) is not None and picture_data.get(curr_year).get(curr_date) is not None:
                        pics_found = picture_data.get(curr_year).get(curr_date)
                        random.shuffle(pics_found)
                        if len(pics_found) > picture_day_limit:
                            pics_found = pics_found[:picture_day_limit]
                            all_pics_found.extend(pics_found)
                        else:
                            all_pics_found.extend(pics_found)

                entry.update({"pic_array": all_pics_found})

    show_pictures()

    return render(request, 'dashboard.html', {'entries': entries})


# restore db from json
@login_required
def restore_db(request):
    # check enviroment
    if os.getenv('GAE_APPLICATION', None) and os.getenv('LOGNAME') != "shef":
        print("running on GCP can't do it that there")
        return
    # validate json by not over writing existing id
    latest_db = os.getenv("JSON_RESTORE_PATH"), shell=True
    latest_db = str(latest_db)[2:25]  # parsing output of script so have
    db_path = os.getenv("json_path") + "/" + latest_db

    entries = Entry.objects.all()

    file = open(db_path)
    with open(db_path, "r") as f:
        all_stories = json.load(f)

    file.close()
    updated_cont = 0
    skip_count = 0
    for input_story in all_stories:
        # title and text inside article has to be unique
        if entries.filter(title=input_story['title']).exists() is False and entries.filter(text=input_story['text']).exists() is False:
            print("found story with new non existing id: " + str(input_story['id']) + " title: " + input_story['title'])
            new_story = Entry()
            new_story.title = input_story['title']
            new_story.date_start = input_story['date_start']
            new_story.date_end = input_story['date_end']
            new_story.text = input_story['text']
            new_story.tags = input_story['tags']
            new_story.save()
            updated_cont += 1
        else:
            print("found existing entity with id: "+ str(input_story['id']) + " title: " + input_story['title'])
            skip_count += 1
    output_msg = "updated: " + str(updated_cont) + " skipped: " + str(skip_count)
    return HttpResponse(output_msg, headers={"SecretCode": "21234567"})


# API end point
class JournalViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        entry = Entry.objects.all().order_by("-id")
        serializer = EntrySerializer(entry, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# TODO
# save data that been submitted by a form
# get information from request that been submitted
# def save_data(received_request):
#     title = received_request.get("title-submit")
#     date_start_str = received_request.get("date-start-submit")
#     date_end_str = received_request.get("date-end-submit")
#     text = received_request.get("text-submit")
#     tags = received_request.get("tags-submit")

#     date_start_date = datetime.datetime.strptime(date_start_str, "%m-%d-%Y").date()
#     date_end_date = datetime.datetime.strptime(date_end_str, "%m-%d-%Y").date()
