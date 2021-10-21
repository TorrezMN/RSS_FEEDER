import npyscreen
 
from forms import ConfigSound
from rss_forms import (AddRssFeed,
                    ListRssFeed)

from articles_forms import (ListArticles,
                            PublishArticle,
                            UpdateArticlesDB,
                            SearchArticles)




def cls():
    npyscreen.blank_terminal()





class App(npyscreen.NPSAppManaged):
    

    def onStart(self):
        self.registerForm("MAIN", MainForm())
        #Feed FORMS
        self.registerForm("ADDFEED", AddRssFeed())
        self.registerForm("LISTFEED", ListRssFeed())
        #Articles FORMS
        self.registerForm("LISTARTICLES", ListArticles())
        self.registerForm("PUBLISHARTICLE", PublishArticle())
        self.registerForm("UPDATEARTICLESDB", UpdateArticlesDB())
        self.registerForm("SEARCHARTICLES", SearchArticles())
        self.registerForm("CONFIGSOUND", ConfigSound())
        
        #System volumen.
        self.systemVolume = 10
        self.read = False
        self.voice_rate = 0

        
class MainForm(npyscreen.FormBaseNewWithMenus, npyscreen.SplitForm):
    def create(self):
        self.name='RSS FEEDER'
        self.add(npyscreen.TitleText, name = "Text:", value= "Hellow World!" )
        #  Menu
        self.menu = self.add_menu(name="Main Menu", shortcut="^M")
        #  RSS FEEDS
        self.rss_submenu = self.menu.addNewSubmenu('RSS', shortcut='r')
        self.rss_submenu.addItem('ADD RSS FEED', self.addform, shortcut='a')
        self.rss_submenu.addItem('LIST RSS FEED', self.listform, shortcut='l')
        #  ARTICLES
        self.articles_submenu = self.menu.addNewSubmenu('ARTICLES', shortcut='a')
        self.articles_submenu.addItem('LIST ARTICLES', self.listarticles, shortcut='l')
        self.articles_submenu.addItem('PUBLISH ARTICLES', self.publishArticle, shortcut='p')
        self.articles_submenu.addItem('SEARCH ARTICLES', self.searchArticles, shortcut='s')
        #  CONFIG
        self.config_menu = self.menu.addNewSubmenu('CONFIG', shortcut='c')
        self.config_menu.addItem('UPDATE ARTICLES DB', self.updatearticlesdb, shortcut='u')
        self.config_menu.addItem('CONFIG SOUND', self.configSound, shortcut='s')
        #  MAIN MENU
        self.menu.addItem('EXIT APP', self.exitAplication, shortcut='s')


        
    def configSound(self):
        
        self.parentApp.switchForm('CONFIGSOUND')
        
    def searchArticles(self):
        
        self.parentApp.switchForm('SEARCHARTICLES')

    def updatearticlesdb(self):
        
        self.parentApp.switchForm('UPDATEARTICLESDB')


    def publishArticle(self):

        self.parentApp.switchForm('PUBLISHARTICLE')

    def listarticles(self):
        self.parentApp.switchForm('LISTARTICLES')


    def addform(self):
        self.parentApp.switchForm('ADDFEED')

    def listform(self):
        self.parentApp.switchForm('LISTFEED')

    def exitAplication(self):
        self.parentApp.switchForm(None)




if __name__ == '__main__':
    TA = App()
    TA.run()
