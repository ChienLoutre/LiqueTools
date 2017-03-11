import nuke
nuke.menu( 'Nodes' ).findItem( 'Deep' ).addCommand( 'DeepOpenEXRId', lambda: nuke.createNode('DeepOpenEXRId') )
import nukes.plugins.liquemenu as liqueplug
liqueplug.lique_menu()
