
Example Extension Package
----

Please see comments in these files and update some values to match 
your extension and to make your package identical: 

- description.xml
- SidebarsByMacros.xcu
- Sidebar.xcu
- META-INF/manifest.xml


## description.xml

You have to edit this file to make your extension package identical to 
your extension. If you do not, it will conflict with some package. 

See the comment in the file.


## SidebarsByMacros.xcu

Your panel have to be registered under "Imples" node with identical name. 

Here is an example with named as "MyPanel1". 

```
   <node oor:name="private:resource/toolpanel/foo.bar/MyPanel1" oor:op="replace">
        <prop oor:name="Initialize">
          <value>vnd.sun.star.script:Standard.Module1.Initialize?location=application&amp;language=Basic</value>
        </prop>
      </node>
```

"Initialize" property defines macro routine to be called when your 
panel being initialized. The name of the routine is not required to 
name "Initialize", any name can be used for your initialization routine.

You can define two or more node having the name you specified to 
add more panels into your deck.


## Sidebar.xcu

This file contains definitions of your decks and panels. 

Here is an example element defined under DeckList.

```
      <node oor:name="MytoolsDeck" oor:op="replace">
        <prop oor:name="Title" oor:type="xs:string">
          <value xml:lang="en-US">My Deck</value>
        </prop>
        <prop oor:name="Id" oor:type="xs:string">
          <value>MytoolsDeck</value>
        </prop>
        <prop oor:name="IconURL" oor:type="xs:string">
          <value>vnd.sun.star.extension://mytools.ui.test.SidebarByMacros/icon1.png</value>
        </prop>
        <prop oor:name="HighContrastIconURL" oor:type="xs:string">
          <value>vnd.sun.star.extension://mytools.ui.test.SidebarByMacros/icon1.png</value>
        </prop>
        <prop oor:name="ContextList">
          <value oor:separator=";">
            Writer, any, visible ;
          </value>
        </prop>
        <prop oor:name="OrderIndex" oor:type="xs:int">
          <value>500</value>
        </prop>
      </node>
    </node>
```

Please change name "MytoolsDeck" to make your deck identical. 
- Title: shown in the top bar of your deck.
- Id: add identical one which makes group of your deck and panels shown in your deck.
- IconURL: deck icon. Preapre 24 x 24 pixel PNG file.
- HighContrastIconURL: the same with the IconURL but with high contrast colors.
- ContextList: See https://wiki.openoffice.org/wiki/Sidebar_for_Developers#Context
- OrderIndex: Order in the deck list GUI, larger order is shown in the lower place.

If you want to show your deck on the specified type of documents, 
set ContextList. You can use names Writer, Calc, Impress and Draw.

Once you define your deck, define your panels next under the PanelList node.
Here is an example panel defined.

```
    <node oor:name="PanelList">
      <node oor:name="MyPanel1" oor:op="replace">
        <prop oor:name="Title" oor:type="xs:string">
          <value xml:lang="en-US">My Panel 1</value>
        </prop>
        <prop oor:name="TitleBarIsOptional" oor:type="xs:boolean">
          <value>false</value>
        </prop>
        <prop oor:name="Id" oor:type="xs:string">
          <value>MyPanel1</value>
        </prop>
        <prop oor:name="DeckId" oor:type="xs:string">
          <value>MytoolsDeck</value>
        </prop>
        <prop oor:name="ContextList">
          <value oor:separator=";">
            Writer, any, visible ;
          </value>
        </prop>
        <prop oor:name="ImplementationURL" oor:type="xs:string">
          <value>private:resource/toolpanel/foo.bar/MyPanel1</value>
        </prop>
        <prop oor:name="OrderIndex" oor:type="xs:int">
          <value>100</value>
        </prop>
      </node>
    </node>
```

"MyPanel1" have to be identical. 
- Title: shown in the top of your panel inside the deck.
- TitleBarIsOptional: if true, no title bar is shown if the deck contains single panel.
- Id: panel Id, make it identical.
- DeckId: this panel is shown in the deck specified by this value.
- ContextList: see the description about the same entry in the deck above.
- ImplementationURL: this value have to be the same with the name defined in SidebarsByMacros.xcu file.
- OrderIndex: smaller value is earlier

You can add multiple definitions of your panels in the file.


## META-INF/manifest.xml

This file lists the package contents which have to be registered by the 
extension manager while installation of your package.

If you put want to pack your macro library in this package, edit the 
following section in the file:

```
<!-- Update this entry to match your library name -->
<manifest:file-entry manifest:full-path="YOUR_LIBRARY/" 
 manifest:media-type="application/vnd.sun.star.basic-library"/>
```

YOUR_LIBRARY is the name of your library.


## Packaging

Copy your library into this directory and update files which described 
above. The time to pack files into OXT package. 

Select all files and make a ZIP archive and rename it to match your 
extension with oxt file extension.

The package contains these files at the root directory of the package. 
If you could not install your package contents, the package structure might 
wrong.
