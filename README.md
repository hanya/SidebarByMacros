
Sidebar by Macros
----

Current implementation of the sidebar requires own UNO-component implementation on OpenOffice. 
This extension provides the helper component to add own sidebar content through macros. 

This extension provides elemental factory for sidebar elements 
written in macros without any UNO component implementations.
This extension works on Apache OpenOffice 4 or newer.
  
Please refere the following pages if you are not familier with terminologies on the sidebar: 
* https://blogs.apache.org/OOo/entry/the_sidebar_new_and_improved
* http://wiki.openoffice.org/wiki/Sidebar_for_Developers


## How to Use

1. Install SidebarHelperForMacros.oxt package through the extension manager.
2. Prepare your panel using Basic IDE dialog editor.
3. Write some code to initialize, see below.
4. Pack your code into extension package. See test/README.md file.
5. Distribute the package.

The following Basic code provides initialization of the desk.
```
' Initialize with UIElement and parent window.
' @param oElement instance that implements css.ui.XUIElement, 
'                 XToolPanel and XSidebarPanel. 
'                 Additionally css.container.XNameContainer that 
'                 allows you to set XSidebarPanel.
' @param oParent parent window
' @return panel window

Function Initialize( oElement as Variant, oParent as Variant ) As Variant
  window = CreateChildWindow("$(user)/basic/Standard/Dialog3.xdl", oParent, True)
  window.setPosSize(0, 0, 0, 0, com.sun.star.awt.PosSize.POS)
  Initialize = window       ' return value
  
  ' If you do not need to set complicated resizing, simply you do not need this.
  oElement.insertByName("XSidebarPanel", _
      CreateUnoListener("XSidebarPanel_", "com.sun.star.ui.XSidebarPanel"))
End Function


Function XSidebarPanel_getHeightForWidth( nWidth as Variant )
  ls = CreateUnoStruct("com.sun.star.ui.LayoutSize")
  ls.Minimum = 150
  ls.Maximum = 150
  ls.Preferred = 150
  XSidebarPanel_getHeightForWidth = ls
End Function

Function CreateChildWindow( sDialogURL as string, oParent as Variant, Optional bMakeVisible as boolean )
  sDialogURI = CreateUnoService("com.sun.star.util.PathSubstitution").substituteVariables(sDialogURL, True)
  dp = CreateUnoService("com.sun.star.awt.ContainerWindowProvider")
  window = dp.createContainerWindow( sDialogURI, "", oParent, Null )
  if not IsNull(window) and Not IsMissing(bMakeVisible) and bMakeVisible then window.setVisible(True)
  CreateChildWindow = window
End Function
```

Initialize function is called while your panel is being created. 
You have to instantiate your window through CreateChildWindow function 
without title bar and return it.

If you have your dialog in your extension package, 
use vnd.sun.star.extension:EXTENSION_ID/path_to_dialog.xdl 
type of URI to specify your dialog file.

This code needs Standard.Dialog3 for the panel content. 
You can not use vnd.sun.star.script protocol to specify your dialog 
for the css.awt.ContainerWindowProvider because of unreported bug.
    
Once you implement the function returns the window that is shown in your panel, 
then you need to add some settings to be shown the panel.


## How to work

When your panel is requested, the registered factory bound to 
the resource URI of your panel is created to generate the real 
instance of the panel shown in the sidebar window. This is done 
by the helper component. 
When the helper takes request to 
make new panel, it searches the configuration: 
/mytools.UI.SidebarsByMacros/Content/Imples/NAME/Initialize
NAME should be the resource URL of your panel.

Once your function is found to initialize, it is called with 
the elements and the parent window as arguments. Your function 
should return the child window to be shown in your panel as a panel.
If you need to responce against dynamic size check, 
implement your own com.sun.star.ui.XSidebarPanel interface as 
described in the above example.
Any other reactions on your panel is the same with 
the actions happen on some awt windows or dialogs.

## Specification

- Prefix for your panel name: private:resource/toolpanel/foo.bar/
- Icon size for the deck: 24 x 24 pixel


## How to make SidebarHelperForMacros
See helper/README.md file.


## License

Public domain. 
  
You can reuse both helper and example code 
in this repository without any notice in your extension.
