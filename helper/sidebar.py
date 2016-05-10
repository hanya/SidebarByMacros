
import uno
import unohelper

from com.sun.star.beans import PropertyValue
from com.sun.star.beans.PropertyState import DIRECT_VALUE
from com.sun.star.container import XNameContainer, NoSuchElementException, ElementExistException
from com.sun.star.lang import XServiceInfo, \
    IllegalArgumentException
from com.sun.star.ui import XUIElementFactory, XUIElement, XToolPanel, XSidebarPanel, \
    LayoutSize
from com.sun.star.ui.UIElementType import TOOLPANEL as UET_TOOLPANEL
from com.sun.star.uno import RuntimeException


class SidebarHelperForMacros(unohelper.Base, XServiceInfo, XUIElementFactory):
    """ Helps to someone implements sidebar components in Macros.
    
        The factory for UI element have to be registered under 
        /org.openoffice.Office.UI.Factories/Registered/UIElementFactories.
        And the components have to be implemented acoording to 
        css.ui.UIElementFactory service.
    """
    
    IMPLE_NAME = "mytools.ui.SidebarHelperForMacros"
    SERVICE_NAMES = IMPLE_NAME,
    
    CONFIG = "/mytools.UI.SidebarsByMacros/Content/Imples"
    
    @staticmethod
    def get():
        klass = SidebarHelperForMacros
        return klass, klass.IMPLE_NAME, klass.SERVICE_NAMES
    
    def __init__(self, ctx, *args):
        self.ctx = ctx
    
    # XServiceInfo
    def getImplementationName(self):
        return self.IMPLE_NAME
    
    def supportsService(self, name):
        return name in self.SERVICE_NAMES
    
    def getSupportedServiceNames(self):
        return self.SERVICE_NAMES
    
    # XUIElementFactory
    def createUIElement(self, res_url, args):
        # see css.ui.XUIElementFactory
        # check the res_url is in the configuration
        settings = self._get_settings(res_url)
        if not settings:
            # no UI element found
            raise NoSuchElementException()
        frame = parent = None
        for arg in args:
            if arg.Name == "Frame":
                frame = arg.Value
            elif arg.Name == "ParentWindow":
                parent = arg.Value
            #elif arg.Name == "Sidebar":
            # If you need css.ui.XSidebar interface to request to 
            # re-layout, keep it.
            #elif arg.Name == "SfxBindings":
            # This is just pointer address, not useful for extensions.
        if not frame:
            raise IllegalArgumentException()
        if not parent:
            raise IllegalArgumentException()
        try:
            # new instance of requested UI element
            return SidebarUIElement(self.ctx, frame, parent, res_url, settings)
        except Exception as e:
            print("Error in SidebarUIElement.ctor: " + str(e))
    
    def _create(self, name):
        return self.ctx.getServiceManager().createInstanceWithContext(name, self.ctx)
    
    def _create_configuration_reader(self, nodepath, res_url):
        cp = self._create("com.sun.star.configuration.ConfigurationProvider")
        try:
            return cp.createInstanceWithArguments( 
                "com.sun.star.configuration.ConfigurationAccess", 
                (PropertyValue("nodepath", -1, nodepath, DIRECT_VALUE),))
        except:
            pass
        return None
    
    def _get_settings(self, res_url):
        reader = self._create_configuration_reader(self.CONFIG, res_url)
        if reader and reader.hasByName(res_url):
            try:
                return reader.getByName(res_url)
            except:
                pass
        return None

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(*SidebarHelperForMacros.get())


class SidebarUIElement(unohelper.Base, XUIElement, XToolPanel, XSidebarPanel, XNameContainer):
    """ Individual panel element in deck of sidebar.
    
        Should be implemented according to css.ui.UIElement service.
        In the case of toolpanel element, you need additional interfaces: 
        - css.ui.XToolPanel: describes panel
        - css.ui.XSidebarPanel: panel (optional, but if not, unusable)
    """
    
    def __init__(self, ctx, frame, parent, res_url, settings):
        self.res_url = res_url
        self.ctx = ctx
        self.frame = frame
        self.parent = parent
        self._values = {}
        try:
            self.window = self._call_macro(settings.Initialize, (self, self.parent))
        except:
            raise RuntimeException("Error while calling Initialize for " + self.res_url, None)
    
    # XUIElement
    @property
    def Frame(self):
        return self.frame
    
    @property
    def ResourceURL(self):
        return self.res_url
    
    @property
    def Type(self):
        return UET_TOOLPANEL
    
    def getRealInterface(self):
        return self # ToDo weakref?
    
    # XToolPanel
    def createAccessible(self, parent):
        return None
    
    @property
    def Window(self):
        return self.window
    
    # XSidebarPanel
    def getHeightForWidth(self, width):
        v = self._values.get("XSidebarPanel", None)
        if v:
            try:
                return v.getHeightForWidth(width)
            except:
                pass
        return LayoutSize(0, -1, 0)
    
    # 
    def _call_macro(self, uri, args=()):
        script = self._create_script_provider().getScript(uri)
        if script:
            try:
                r ,_ ,_ = script.invoke(args, (), ())
                return r
            except Exception as e:
                print(e)
        return None
    
    def _create_script_provider(self):
        mspf = self.ctx.getValueByName(
            "/singletons/com.sun.star.script.provider.theMasterScriptProviderFactory")
        return mspf.createScriptProvider("")
        # ToDo language specific script provider
    
    # XNameContainer
    # this interface is not required by the panel, just for helper
    def insertByName(self, name, value):
        if name in self._values:
            raise ElementExistException(name, self)
        else:
            self._values[name] = value
    
    def removeByName(self, name):
        if name in self._values:
            self._values.pop(name)
        else:
            raise NoSuchElementException(name, self)
    
    def replaceByName(self, name, value):
        if name in self._values:
            self._values[name] = value
        else:
            raise NoSuchElementException(name, self)
    
    def getByName(self, name):
        try:
            return self._values[name]
        except:
            raise NoSuchElementException(name, self)
    
    def getElementNames(self):
        return tuple(self._values.names())
    
    def hasByName(self, name):
        return name in self._values
    
    def getElementType(self):
        return uno.getTypeByName("any")
    
    def hasElements(self):
        return len(self._values) != 0
