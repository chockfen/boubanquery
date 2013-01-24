# -*- coding: utf-8 -*-
import wx
from douban_client import DoubanClient
import httplib2
import urllib2
import urllib
import json
import os

save_path = "image"
class MyApp(wx.App):
    def OnInit(self):
        self.START = 0
        self.TOTAL = 0
        self.COUNT = 2
        self.frame = wx.Frame(parent = None, title = 'Douban Reader', size=(480,600))
        
        self.panel = wx.Panel(self.frame, -1)
        #标题
        title = wx.StaticText(self.panel, -1, 'Douban Reader',
                              style = wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL,
                              size = (480,50))
        title.SetFont(wx.Font(15,wx.SWISS,wx.NORMAL,wx.BOLD))
        title.SetForegroundColour('white')
        title.SetBackgroundColour('grey')
        #输入框,搜索按钮
        self.bookName = wx.TextCtrl(self.panel, -1,u"请输入需要查询的书籍名", pos = (10,60), size = (350,20))
        self.buttonOk = wx.Button(self.panel, -1, 'search', pos = (370,60))
        self.Bind(wx.EVT_BUTTON, self.OnButtonOK, self.buttonOk)

        #===================================
        
        
        #===================================

        #布局
        #垂直的sizer========
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(title,0,wx.EXPAND)
        
        #搜索sizer
        searchSizer = wx.FlexGridSizer(cols=2,hgap=5,vgap=5)
        searchSizer.AddGrowableCol(0)
        searchSizer.AddGrowableCol(1)
        searchSizer.Add(self.bookName,1,
                        wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND)
        searchSizer.Add(self.buttonOk,1,wx.EXPAND)
        
        self.mainSizer.Add(searchSizer,0,wx.EXPAND|wx.ALL,10)
        #分割线
        self.mainSizer.Add(wx.StaticLine(self.panel),0,wx.EXPAND|wx.TOP|wx.BOTTOM,5)
        #======================================
        self.footSizer = wx.FlexGridSizer(cols=2,hgap=5,vgap=5)
        self.footSizer.AddGrowableCol(0)
        self.footSizer.AddGrowableCol(1)
        
        self.mainSizer.Add(self.footSizer,0,wx.EXPAND)
        self.mainSizer.Add(wx.StaticLine(self.panel),0,wx.EXPAND|wx.TOP|wx.BOTTOM,5)
        #======================================
        #书籍信息显示
        self.bookInfoSizer = wx.FlexGridSizer(cols=2,hgap=5,vgap=5)
        self.bookInfoSizer.AddGrowableCol(1)
        
        self.mainSizer.Add(self.bookInfoSizer)
        
        self.panel.SetSizer(self.mainSizer)
        #self.mainSizer.Fit(self.frame)
        #self.mainSizer.SetSizeHints(self.frame)
        self.frame.Show()

        return True

    def IfPage(self):
        self.frame.Refresh()
        self.footSizer.DeleteWindows()
        self.footSizer.Clear()
        if self.TOTAL != 0:
            if (self.TOTAL - self.START)> self.COUNT:
                self.btnDown = wx.Button(self.panel, -1,"next" , pos=(200,100))
                self.Bind(wx.EVT_BUTTON, self.OnBtnDown, self.btnDown)
                if self.START == 0 :
                    self.footSizer.Add(self.btnDown,wx.EXPAND)
                else:
                    self.btnUp = wx.Button(self.panel, -1,"forword" , pos=(100,100))
                    self.Bind(wx.EVT_BUTTON, self.OnBtnUp, self.btnUp)
                    self.footSizer.Add(self.btnUp,1,wx.EXPAND)
                    self.footSizer.Add(self.btnDown,1,wx.EXPAND)
            else:
                self.btnUp = wx.Button(self.panel, -1,"forword" , pos=(100,100))
                self.Bind(wx.EVT_BUTTON, self.OnBtnUp, self.btnUp)
                self.footSizer.Add(self.btnUp,1,wx.EXPAND)

    #==========================上一页
    def OnBtnUp(self,event):
        self.bookInfoSizer.DeleteWindows()
        self.bookInfoSizer.Clear()
        self.START -= 2
        wx.MessageBox(str(self.START),"up",wx.OK)
        book = self.search_book(self.bookName.GetValue(),self.START,self.COUNT)
        bookInfo = ''
        bookInfo2 = ''
        #==========================================================================无数据显示
        if len(book) == 0:
            bookInfo = u"\n暂无结果╮(╯▽╰)╭"
            info = wx.StaticText(self.panel, -1, bookInfo,
                                     style = wx.TE_WORDWRAP|wx.ALIGN_CENTRE_VERTICAL,
                                     pos = (5,100))
            self.bookInfoSizer.Add(info)
            info.SetForegroundColour('grey')
            font = wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL)
            info.SetFont(font)
        else:
            #wx.MessageBox('Result:'+book[0]["title"],'wxPython',wx.OK)          
            for i in range(len(book)):
                bookInfo = ("\n" + str(i+1) +
                         u": 标题： " + book[i]["title"] +
                          u"\n作者： " + book[i]["author"][0])
                #==============================================================
                bImage = self.get_image(str(book[i]["images"]["medium"]),book[i]["id"],save_path)
                
                sb = wx.StaticBitmap(self.panel, -1, bImage,pos = (5,5))
                info = wx.StaticText(self.panel, -1, bookInfo,
                                     style = wx.TE_WORDWRAP,
                                     pos = (5,100),
                                     size = (330,200))
                info.SetForegroundColour('grey')
                font = wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL)
                info.SetFont(font)
                self.bookInfoSizer.Add(sb)
                self.bookInfoSizer.Add(info)
                self.panel.Refresh()
        self.IfPage()
        self.frame.Refresh()
        self.mainSizer.Fit(self.frame)

        
    #==========================下一页
    def OnBtnDown(self,event):
        self.bookInfoSizer.DeleteWindows()
        self.bookInfoSizer.Clear()
        self.START += 2
        wx.MessageBox(str(self.START),"down",wx.OK)
        book = self.search_book(self.bookName.GetValue(),self.START,self.COUNT)
        bookInfo = ''
        bookInfo2 = ''
        #==========================================================================无数据显示
        if len(book) == 0:
            bookInfo = u"\n暂无结果╮(╯▽╰)╭"
            info = wx.StaticText(self.panel, -1, bookInfo,
                                     style = wx.TE_WORDWRAP|wx.ALIGN_CENTRE_VERTICAL,
                                     pos = (5,100))
            self.bookInfoSizer.Add(info)
            info.SetForegroundColour('grey')
            font = wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL)
            info.SetFont(font)
        else:
            #wx.MessageBox('Result:'+book[0]["title"],'wxPython',wx.OK)          
            for i in range(len(book)):
                bookInfo = ("\n" + str(i+1) +
                         u": 标题： " + book[i]["title"] +
                          u"\n作者： " + book[i]["author"][0])
                #==============================================================
                bImage = self.get_image(str(book[i]["images"]["medium"]),book[i]["id"],save_path)
                
                sb = wx.StaticBitmap(self.panel, -1, bImage,pos = (5,5))
                info = wx.StaticText(self.panel, -1, bookInfo,
                                     style = wx.TE_WORDWRAP,
                                     pos = (5,100),
                                     size = (330,200))
                info.SetForegroundColour('grey')
                font = wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL)
                info.SetFont(font)
                self.bookInfoSizer.Add(sb)
                self.bookInfoSizer.Add(info)
                self.panel.Refresh()
        self.IfPage()
        self.frame.Refresh()
        self.mainSizer.Fit(self.frame)
    
    #查询图书，返回书籍列表
    def search_book(self,book,start,count):
        self.bookInfoSizer.Clear()
        h = httplib2.Http()
        url_search = "https://api.douban.com/v2/book/search"+"?q="+book+"&start="+str(start)+"&count="+str(count)
        resp, content = h.request(url_search,"GET")
        s = json.loads(content,encoding="utf-8")
        self.TOTAL = s['total']
        return s['books']
    
    #查询按钮
    def OnButtonOK(self,event):
        #查询书籍信息
        self.bookInfoSizer.DeleteWindows()
        self.bookInfoSizer.Clear()
        self.START=0
        book = self.search_book(self.bookName.GetValue(),0,self.COUNT)
        bookInfo = ''
        bookInfo2 = ''
        #==========================================================================无数据显示
        if len(book) == 0:
            bookInfo = u"\n暂无结果╮(╯▽╰)╭"
            info = wx.StaticText(self.panel, -1, bookInfo,
                                     style = wx.TE_WORDWRAP|wx.ALIGN_CENTRE_VERTICAL,
                                     pos = (5,100))
            self.bookInfoSizer.Add(info)
            info.SetForegroundColour('grey')
            font = wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL)
            info.SetFont(font)
        else:
            #wx.MessageBox('Result:'+book[0]["title"],'wxPython',wx.OK)          
            for i in range(len(book)):
                bookInfo = ("\n" + str(i+1) +
                         u": 标题： " + book[i]["title"] +
                          u"\n作者： " + book[i]["author"][0])
                #==============================================================
                bImage = self.get_image(str(book[i]["images"]["medium"]),book[i]["id"],save_path)
                
                sb = wx.StaticBitmap(self.panel, -1, bImage,pos = (5,5))
                info = wx.StaticText(self.panel, -1, bookInfo,
                                     style = wx.TE_WORDWRAP,
                                     pos = (5,100),
                                     size = (330,200))
                info.SetForegroundColour('grey')
                font = wx.Font(10,wx.SWISS,wx.NORMAL,wx.NORMAL)
                info.SetFont(font)
                self.bookInfoSizer.Add(sb)
                self.bookInfoSizer.Add(info)
                self.panel.Refresh()
        self.IfPage()
        self.frame.Refresh()
        self.mainSizer.Fit(self.frame)

    #下载图片
    def get_image(self,file_url, file_name,save_path):
        filename = save_path + "\\" + file_name +".jpg"
        urllib.urlretrieve(file_url,filename)     
        imgdata = wx.Image(filename, wx.BITMAP_TYPE_ANY)
        bImage = wx.BitmapFromImage(imgdata)        
        return bImage
    
app = MyApp()
app.MainLoop()
