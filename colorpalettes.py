from flask import Flask, render_template, json, request, send_from_directory
import numpy as np
import pandas as pd
import matplotlib
import json
import random
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import mpld3
from mpld3 import plugins, utils
import requests
import colorutils
from colorutils import Color
import itertools
import threading
import time
import sys
from bs4 import BeautifulSoup

def draw_fig(info):

        css = """
        .boxed {
          font-family:Arial, Helvetica, sans-serif;
          font-size:12px;
          background-color: rgba(255,255,255, 0.8);
          padding: 10px;
        }

        g.mpld3-xaxis, g.mpld3-yaxis {
        display: none;
        }
        """

        base_url = "https://api.harvardartmuseums.org/object"

        payload = {
                'sort': 'random',
                }

        with open('apikey.json') as f:
            apikey = json.load(f)
            payload['apikey'] = apikey['apikey']

        for key, value in info.items():
            payload[key] = value

        r = requests.get(base_url, params=payload)

        data = json.loads(r.text)

        print('got the data in script')

        works_with_color = []
        each_work = {}

        list = data['records']

        if len(list) == 0:

            emptydata = {}
            emptylist = []
            emptydata[0] = render_template('nonefound.html')
            emptydata[1] = emptylist
            return emptydata

        imageworkslist = []

        for record in list:
            if (('primaryimageurl' != None) and ('colors' in record)):
                    imageworkslist.append(record)

        for record in imageworkslist:
            if 'colors' in record:
                works_with_color.append(record)

        listcycle = itertools.cycle(works_with_color)

        artistlist = []
        datelist = []
        techniquelist = []
        image_url_list = []
        collections_url_list = []

        print('other things happened')

        for idx, work in enumerate(works_with_color):
            subcolors = {}
            testlist = []
            saturationlist = []
            for color in work['colors']:
                testlist.append(color['color'])
                subcolors[color['color']] = color['percent']
                for item in testlist:
                    c = Color(hex=item)
                    saturationlist.append(c.hsv[1])
            avg = sum(saturationlist)/len(saturationlist)
            if (avg == 0):
                next(listcycle)
            else:
                each_work[work['title']] = subcolors
                if 'people' in work:
                    if work['people'][0]['culture'] is not None:
                        if work['people'][0]['displaydate'] is not None:
                            artistlist.append(str(work['people'][0]['name'])+" ("+str(work['people'][0]['culture'])+", "+str(work['people'][0]['displaydate'])+")")
                        else:artistlist.append(str(work['people'][0]['name'])+" ("+str(work['people'][0]['culture'])+")")
                    else:
                        artistlist.append(str(work['people'][0]['name']))
                else:
                    artistlist.append('Unidentified Artist')
                if 'dated' in work and work['dated'] is None:
                    datelist.append('n.d.')
                else:
                    datelist.append(work['dated'])
                if work['technique'] is not None:
                    techniquelist.append(work['technique'])
                else:
                    if work['medium'] is not None:
                        techniquelist.append(work['medium'])
                    else:
                        if work['classification'] is not None:
                            classification = work['classification']
                            classification = classification.rstrip('s')
                            techniquelist.append(classification)
                        else:
                            techniquelist.append(work['department'])
                if len(work['images']) != 0 and 'idsid' in work['images'][0]:
                    collections_url_list.append(work['url'])
                    image_url_list.append("https://ids.lib.harvard.edu/ids/view/"+str(work['images'][0]['idsid']))
                else:
                    print('the soup part started')
                    collection_item_url = work['url']
                    try:
                        req = requests.get(collection_item_url, timeout=.01)
                        soup = BeautifulSoup(req.content, 'html.parser')
                        idsid = soup.find("div", {'class':'osd'})['data-initial-image-id']
                        image_url_list.append("https://ids.lib.harvard.edu/ids/view/"+str(idsid))
                        collections_url_list.append(work['url'])
                    except requests.Timeout as err:
                        print('timeout process happened')
                        image_url_list.append("static/css/images/noimage.png")
                        collections_url_list.append("https://jackp2021.github.io/HAMnotfound.html")



        urls = image_url_list
        coll_urls = collections_url_list
        r = lambda: random.randint(0,255)
        for key in each_work:
            while len(each_work[key])<10:
                each_work[key]['#%02X%02X%02X' % (r(),r(),r())] = 0

        nameList = []
        colorList = []
        percentList = []

        for i in each_work:
            nameList.append(i)
            colors = []
            percents = []
            for item in each_work[i]:
                colors.append(item)
                percents.append(each_work[i][item])
            colorList.append(colors)
            percentList.append(percents)

        colorArray = np.array(colorList)
        percentArray = np.array(percentList)

        print('graph data lists have been created')

        labels = nameList
        first_color = colorArray[:,0]
        first_percent = percentArray[:,0]
        second_color = colorArray[:,1]
        second_percent = percentArray[:,1]
        third_color = colorArray[:,2]
        third_percent = percentArray[:,2]
        fourth_color = colorArray[:,3]
        fourth_percent = percentArray[:,3]
        fifth_color = colorArray[:,4]
        fifth_percent = percentArray[:,4]
        sixth_color = colorArray[:,5]
        sixth_percent = percentArray[:,5]
        seventh_color = colorArray[:,6]
        seventh_percent = percentArray[:,6]
        eigth_color = colorArray[:,7]
        eigth_percent = percentArray[:,7]
        ninth_color = colorArray[:,8]
        ninth_percent = percentArray[:,8]
        tenth_color = colorArray[:,9]
        tenth_percent = percentArray[:,9]

        width = 0.7

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)

        for i, item in enumerate(first_percent):
            height = first_percent[i]+second_percent[i]+third_percent[i]+fourth_percent[i]+fifth_percent[i]+sixth_percent[i]+seventh_percent[i]+eigth_percent[i]+ninth_percent[i]+tenth_percent[i]
            if height < 1:
                first_percent[i] += 1-height


        ax.bar(labels, first_percent, width, color=first_color)
        ax.bar(labels, second_percent, width, bottom=first_percent, color=second_color)
        ax.bar(labels, third_percent, width, bottom=(second_percent+first_percent), color=third_color)
        ax.bar(labels, fourth_percent, width, bottom=(second_percent+first_percent+third_percent), color=fourth_color)
        ax.bar(labels, fifth_percent, width, bottom=(second_percent+first_percent+third_percent+fourth_percent), color=fifth_color)
        ax.bar(labels, sixth_percent, width, bottom=(second_percent+first_percent+third_percent+fourth_percent+fifth_percent), color=sixth_color)
        ax.bar(labels, seventh_percent, width, bottom=(second_percent+first_percent+third_percent+fourth_percent+fifth_percent+sixth_percent), color=seventh_color)
        ax.bar(labels, eigth_percent, width, bottom=(second_percent+first_percent+third_percent+fourth_percent+fifth_percent+sixth_percent+seventh_percent), color=eigth_color)
        ax.bar(labels, ninth_percent, width, bottom=(second_percent+first_percent+third_percent+fourth_percent+fifth_percent+sixth_percent+seventh_percent+eigth_percent), color=ninth_color)
        ax.bar(labels, tenth_percent, width, bottom=(second_percent+first_percent+third_percent+fourth_percent+fifth_percent+sixth_percent+seventh_percent+eigth_percent+ninth_percent), color=tenth_color)

        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        plt.xticks([], [])
        plt.yticks([], [])
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.set_facecolor('#f8f8f8')

        print('graph has been created')

        class ClickInfo(plugins.PluginBase):
            """Plugin for getting info on click"""

            JAVASCRIPT = """
            mpld3.register_plugin("clickinfo", ClickInfo);
            ClickInfo.prototype = Object.create(mpld3.Plugin.prototype);
            ClickInfo.prototype.constructor = ClickInfo;
            ClickInfo.prototype.requiredProps = ["id", "urls", "coll_urls"];
            function ClickInfo(fig, props){
                mpld3.Plugin.call(this, fig, props);
            };

            ClickInfo.prototype.draw = function(){
                var obj = mpld3.get_element(this.props.id);
                var urls = this.props.urls;
                var coll_urls = this.props.coll_urls;
                obj.elements().on("mousedown",function(d, i){
                                    if (d3.event.shiftKey) {
                                    window.open(coll_urls[i], '_blank')}
                                    else {
                                    window.open(urls[i], '_blank')
                                    }
                                    });
            }
            """

            def __init__(self, line, url=None, coll_url=None):
                self.bars = line
                self.urls = urls
                self.coll_urls = coll_urls
                self.dict_ = {"type": "clickinfo",
                              "id": mpld3.utils.get_id(line),
                              "urls": url if url is None else [url],
                              "coll_urls": coll_url if coll_url is None else [coll_url]}

        fullbars = [1] * len(labels)
        bars = plt.bar(labels, fullbars, alpha = 0)
        labels2 = []

        for idx, i in enumerate(labels):

            labels2.append("<div class ='boxed'>"+artistlist[idx]+"<br><b>"+i+"</b><br>"+str(techniquelist[idx])+"<br>"+str(datelist[idx])+"<br><img src='"+str(urls[idx])+"' width='75'></div>")

        for i, bar in enumerate(bars.get_children()):
            tooltip = mpld3.plugins.LineHTMLTooltip(bar, label=labels2[i], css=css)
            mpld3.plugins.connect(plt.gcf(), tooltip)

        for i, bar in enumerate(bars.get_children()):
            mpld3.plugins.connect(plt.gcf(), ClickInfo(bar, url=urls[i], coll_url=coll_urls[i]))

        returndata = {}
        returndata[0] = mpld3.fig_to_html(fig)
        returndata[1] = urls
        return returndata

        print('got to end of fig script')
        # return mpld3.fig_to_html(fig)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    print('huh?')
    data = json.loads(request.data)
    print('loaded request')
    return draw_fig(data)
    print('data has sent')




if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0')
