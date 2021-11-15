# coding: utf-8

# In[ ]:


import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter.filedialog import askdirectory
from PIL import ImageTk
import os
import requests
# from bs4 import BeautifulSoup
import random
import json
import emoji
from instagram_scraper.app import InstagramScraper


class args_test():
    def __init__(self, username='', usernames=[], filename=None,
                 login_user=None, login_pass=None,
                 followings_input=False, followings_output=None,
                 destination='./', logger=None, retain_username=False, interactive=False,
                 quiet=False, maximum=0, media_metadata=False, profile_metadata=False, latest=False,
                 latest_stamps=False, cookiejar=None, filter_location=None, filter_locations=None,
                 media_types=['image', 'video', 'story-image', 'story-video', 'broadcast'],
                 tag=False, location=False, search_location=False, comments=False,
                 verbose=0, include_location=False, filter=None, proxies={}, no_check_certificate=False,
                 template='{urlname}', log_destination='', filter_location_file=None, retry_forever=False):
        self.username = str(username)
        self.usernames = usernames
        self.filename = filename
        self.login_user = login_user
        self.login_pass = login_pass
        self.followings_input = followings_input
        self.followings_output = followings_output
        self.destination = destination
        self.logger = logger
        self.retain_username = retain_username
        self.interactive = interactive
        self.quiet = quiet
        self.maximum = maximum
        self.media_metadata = media_metadata
        self.profile_metadata = profile_metadata
        self.latest = latest
        self.latest_stamps = latest_stamps
        self.cookiejar = cookiejar
        self.filter_location = filter_location
        self.filter_locations = filter_locations
        self.media_types = media_types
        self.tag = tag
        self.location = location
        self.search_location = search_location
        self.comments = comments
        self.verbose = verbose
        self.include_location = include_location
        self.filter = None
        self.proxies = proxies
        self.no_check_certificate = no_check_certificate
        self.template = template
        self.log_destination = log_destination
        self.filter_location_file = filter_location_file
        self.retry_forever = retry_forever


class IG_Photo_Parser(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        f = tkFont.Font(size=16, family="Times New Roman")
        self.grid()
        self.btn_Select_Parser = tk.Button(self, text="Parser?", height=5, width=15, font=f, command=self.createWidgets_Parser)
        self.btn_Select_Parser.grid(row=0, column=6, sticky=tk.NE + tk.SW)
        self.btn_Select_Lottery = tk.Button(self, text="Lottery?", height=5, width=15, font=f, command=self.createWidgets_Lottery)
        self.btn_Select_Lottery.grid(row=0,column=12,sticky=tk.NE + tk.SW)

    def createWidgets_Parser(self):
        self.grid()
        self.btn_Select_Parser.destroy()
        self.btn_Select_Lottery.destroy()
        f = tkFont.Font(size=16, family="Times New Roman")
        # UserName
        self.lbl_UserName = tk.Label(self, text="Target_name*", height=1, width=20, font=f)
        self.txt_UserName = tk.Text(self, height=1, width=20, font=f)
        self.lbl_UserName.grid(row=0, column=0, sticky=tk.NE + tk.SW)
        self.txt_UserName.grid(row=0, column=1, columnspan=5, sticky=tk.NE + tk.SW)

        # Login_Username
        self.lbl_Login_Username = tk.Label(self, text="Username", height=1, width=20, font=f)
        self.txt_Login_Username = tk.Text(self, height=1, width=20, font=f)
        self.lbl_Login_Username.grid(row=1, column=0, sticky=tk.NE + tk.SW)
        self.txt_Login_Username.grid(row=1, column=1, columnspan=5, sticky=tk.NE + tk.SW)

        # Login_Password
        self.lbl_Login_Password = tk.Label(self, text="Password", height=1, width=20, font=f)
        self.txt_Login_Password = tk.Text(self, height=1, width=20, font=f)
        self.lbl_Login_Password.grid(row=2, column=0, sticky=tk.NE + tk.SW)
        self.txt_Login_Password.grid(row=2, column=1, columnspan=5, sticky=tk.NE + tk.SW)

        self.lbl_Num = tk.Label(self, text="Amount", height=1, width=20, font=f)
        self.entry_Num = tk.Entry(self, textvariable=IntVar, width=20, font=f)
        self.lbl_Num.grid(row=3, column=0, sticky=tk.NE + tk.SW)
        self.entry_Num.grid(row=3, column=1, columnspan=5, sticky=tk.NE + tk.SW)
        
        self.lbl_Category = tk.Label(self, text="Category", height=1, width=20, font=f)
        self.Category_post_image = BooleanVar()
        self.Category_post_video = BooleanVar()
        self.Category_story_image = BooleanVar()
        self.Category_story_video = BooleanVar()
        self.Category_broadcast = BooleanVar()

        self.CheckBtn_Category_post_image = tk.Checkbutton(self, text="Post_Image", variable=self.Category_post_image,
                                                           onvalue=True, offvalue=False)
        self.CheckBtn_Category_post_video = tk.Checkbutton(self, text="Post_Video", variable=self.Category_post_video,
                                                           onvalue=True, offvalue=False)
        self.CheckBtn_Category_story_image = tk.Checkbutton(self, text="Story_Image", variable=self.Category_story_image,
                                                            onvalue=True, offvalue=False)
        self.CheckBtn_Category_story_video = tk.Checkbutton(self, text="Story_Video", variable=self.Category_story_video,
                                                            onvalue=True, offvalue=False)
        self.CheckBtn_Category_broadcast = tk.Checkbutton(self, text="Livestream", variable=self.Category_broadcast,
                                                          onvalue=True, offvalue=False)

        self.lbl_Category.grid(row=4, column=0, sticky=tk.NE + tk.SW)
        self.CheckBtn_Category_post_image.grid(row=4, column=1, sticky=tk.NE + tk.SW)
        self.CheckBtn_Category_post_video.grid(row=4, column=2, sticky=tk.NE + tk.SW)
        self.CheckBtn_Category_story_image.grid(row=4, column=3, sticky=tk.NE + tk.SW)
        self.CheckBtn_Category_story_video.grid(row=4, column=4, sticky=tk.NE + tk.SW)
        self.CheckBtn_Category_broadcast.grid(row=4, column=5, sticky=tk.NE + tk.SW)

        self.path = StringVar()
        self.lbl_Directory = tk.Label(self, text="Target_Path", height=1, width=20, font=f)
        self.entry_Directory = tk.Entry(self, textvariable=self.path, width=20, font=f)
        self.btn_Directory = tk.Button(self, text="Path", height=1, width=20, font=f, command=self.clickbtnSlectPath)
        self.lbl_Directory.grid(row=6, column=0, sticky=tk.NE + tk.SW)
        self.entry_Directory.grid(row=6, column=1, columnspan=5, sticky=tk.NE + tk.SW)
        self.btn_Directory.grid(row=6, column=6, sticky=tk.NE + tk.SW)

        # Paeser Button
        self.btnParser = tk.Button(self, text="Parser!", height=1, width=5, font=f, command=self.clickbtnParser)
        self.btnParser.grid(row=0, column=6, sticky=tk.NE + tk.SW)

    def createWidgets_Lottery(self):
        f = tkFont.Font(size=16, family="Times New Roman")
        self.btn_Select_Parser.destroy()
        self.btn_Select_Lottery.destroy()
        
        self.lbl_Lottery = tk.Label(self, text="Lottery！", height=1, width=20, font=f)
        self.lbl_Lottery_Url = tk.Label(self, text="Website of Post", height=1, width=20, font=f)
        self.txt_Lottery_Url = tk.Text(self, height=1, width=20, font=f)
        self.lbl_Lottery_Num = tk.Label(self, text="Amount", height=1, width=20, font=f)
        self.lbl_Result = tk.Label(self, text="Result:", height=1, width=20, font=f)
        self.entry_Lottery_Num = tk.Entry(self, textvariable=IntVar, width=20, font=f)

        self.Bool_Duplicate = BooleanVar()
        self.CheckBtn_Duplicate = tk.Checkbutton(self, text="Do the same comments count？", variable=self.Bool_Duplicate,
                                                 onvalue=True,
                                                 offvalue=False)

        self.lbl_Lottery.grid(row=7, column=1, columnspan=5, sticky=tk.NE + tk.SW)
        self.lbl_Lottery_Url.grid(row=8, column=0)
        self.txt_Lottery_Url.grid(row=8, column=1, columnspan=5, sticky=tk.NE + tk.SW)
        self.lbl_Lottery_Num.grid(row=9, column=0)
        self.lbl_Result.grid(row=10, column=0)
        self.entry_Lottery_Num.grid(row=9, column=1, columnspan=5, sticky=tk.NE + tk.SW)
        self.CheckBtn_Duplicate.grid(row=8, column=6)

        self.btn_Lottery = tk.Button(self, text="Draw！", height=1, width=20, font=f, command=self.clickbtnLottery)
        self.btn_Lottery.grid(row=9, column=6, sticky=tk.NE + tk.SW)

        self.lottery_result = tk.StringVar()
        self.lb_lottery = tk.Listbox(self, listvariable=self.lottery_result)
        self.lb_lottery.grid(row=10, column=1, columnspan=5, sticky=tk.NE + tk.SW)


    def clickbtnSlectPath(self):
        self.path_revised = askdirectory()
        self.path.set(self.path_revised)

    def get_input_information(self):
        username_input = self.txt_UserName.get("1.0", tk.END).strip()
        try:
            Max_Num_input = int(self.entry_Num.get())
        except:
            Max_Num_input = 0 
        Login_Username_input = self.txt_Login_Username.get("1.0", tk.END).strip()
        Login_Password_input = self.txt_Login_Password.get("1.0", tk.END).strip()
        destination_input = self.path.get()

        media_types_input = ""
        if self.Category_post_image.get() == True:
            media_types_input += "image"
        if self.Category_post_video.get() == True:
            media_types_input += "video"
        if self.Category_story_image.get() == True:
            media_types_input += "story_image"
        if self.Category_story_video.get() == True:
            media_types_input += "story_video"
        if self.Category_broadcast.get() == True:
            media_types_input += "broadcast"
        if len(media_types_input) == 0:
            media_types_input = ['image', 'video', 'story-image', 'story-video', 'broadcast']

        return username_input, Max_Num_input, Login_Username_input, Login_Password_input, destination_input, media_types_input

    def clickbtnParser(self):
        username_input, Max_Num_input, Login_Username_input, Login_Password_input, destination_input, media_types_input = self.get_input_information()

        args = args_test(username=username_input,
                         login_user=Login_Username_input,
                         login_pass=Login_Password_input,
                         maximum=Max_Num_input,
                         destination=destination_input,
                         media_types=media_types_input,
                         comments=True)

        if (args.login_user and args.login_pass is None) or (args.login_user is None and args.login_pass):
            parser.print_help()
            raise ValueError('Must provide login user AND password')

        if not args.username and args.filename is None and not args.followings_input:
            parser.print_help()
            raise ValueError(
                'Must provide username(s) OR a file containing a list of username(s) OR pass --followings-input')
        elif (args.username and args.filename) or (args.username and args.followings_input) or (
                args.filename and args.followings_input):
            parser.print_help()
            raise ValueError(
                'Must provide only one of the following: username(s) OR a filename containing username(s) OR --followings-input')
        if args.tag and args.location:
            parser.print_help()
            raise ValueError('Must provide only one of the following: hashtag OR location')
        if args.tag and args.filter:
            parser.print_help()
            raise ValueError('Filters apply to user posts')

        if (args.filter_location or args.filter_location_file) and not args.include_location:
            parser.print_help()
            raise ValueError('Location filter needs locations in metadata to filter properly')

        if args.filename:
            args.usernames = InstagramScraper.get_values_from_file(args.filename)

        else:
            args.usernames = [args.username]

        if args.filter_location_file:
            args.filter_locations = InstagramScraper.get_locations_from_file(args.filter_location_file)
        elif args.filter_location:
            locations = {}
            locations.setdefault('', [])
            locations[''] = InstagramScraper.parse_delimited_str(','.join(args.filter_location))
            args.filter_locations = locations

        if args.media_types and len(args.media_types) == 1 and re.compile(r'[,;\s]+').findall(args.media_types[0]):
            args.media_types = InstagramScraper.parse_delimited_str(args.media_types[0])

        if args.retry_forever:
            global MAX_RETRIES
            MAX_RETRIES = sys.maxsize

        scraper = InstagramScraper(**vars(args))

        if args.login_user and args.login_pass:
            scraper.authenticate_with_login()
        else:
            scraper.authenticate_as_guest()
        #
        if args.followings_input:
            scraper.usernames = list(scraper.query_followings_gen(scraper.login_user))
            if args.followings_output:
                with open(scraper.destination + scraper.followings_output, 'w') as file:
                    for username in scraper.usernames:
                        file.write(username + "\n")
                # If not requesting anything else, exit
                if args.media_types == ['none'] and args.media_metadata is False:
                    scraper.logout()
                    pass

        if args.tag:
            scraper.scrape_hashtag()
        elif args.location:
            scraper.scrape_location()
        elif args.search_location:
            scraper.search_locations()
        else:
            scraper.scrape()

        scraper.save_cookies()

        self.posts = scraper.posts
        self.username = username_input

    def get_shortcode(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        attr = {"type": "text/javascript"}
        tag = soup.find("script", attrs=attr, text=re.compile('window\._sharedData')) 

        revised_tag = tag.string.partition('=')[-1].strip(' ;')
        result = json.loads(revised_tag)
        shortcode = result["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]["shortcode"]
        return shortcode

    def clickbtnLottery(self):
        self.lb_lottery.delete(0, "end")
        url = self.txt_Lottery_Url.get("1.0", tk.END).strip()
        shortcode = self.get_shortcode(url)
        withdral_name_list = []
        withdral_content_list = []
        for post in self.posts:
            if post["shortcode"] == shortcode:
                for comment in post["comments"]["data"]:
                    if comment["owner"]["username"] != self.username:
                        withdral_name_list.append(comment["owner"]["username"])
                        withdral_content_list.append(emoji.demojize(comment["text"]))
                break

        try:
            Lottery_Num = int(self.entry_Lottery_Num.get())
        except:
            Lottery_Num = 3  

        withdraw_dict = dict()
        lottery_result_list = []
        for i in range(0, len(withdral_name_list)):
            if withdral_name_list[i] not in withdraw_dict.keys():
                withdraw_dict[withdral_name_list[i]] = [withdral_content_list[i]]
            elif withdral_name_list[i] in withdraw_dict.keys():
                withdraw_dict[withdral_name_list[i]].append(withdral_content_list[i])

        if self.Bool_Duplicate.get() == True:
            start = 0
            end = len(withdral_name_list)
            rand_seq = range(start, end)
            result_index = random.choices(rand_seq, k=Lottery_Num)  
            for i in range(0, Lottery_Num):
                all_comment = ""
                for comment in withdraw_dict[withdral_name_list[result_index[i]]]:
                    all_comment += comment + "/"
                lottery_result_list.append("Winner：" + withdral_name_list[result_index[i]] + "；context：" + all_comment[:-1])

        elif self.Bool_Duplicate.get() == False: 
            result_name_list = random.sample(withdraw_dict.keys(),
                                             k=Lottery_Num)  # random.sample(rand_seq, k = Lottery_Num)  
            for name in result_name_list:
                lottery_result_list.append("Winner：" + name + "；context：" + withdraw_dict[name][-1])

        for item in lottery_result_list:
            self.lb_lottery.insert("end", item)


p1 = IG_Photo_Parser()
p1.master.title("Instagram Parser")
p1.mainloop()
