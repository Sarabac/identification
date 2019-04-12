<h1>Identification</h1>
<h2>To identify Animals on a camera trap picture.</h2>
<p>
This application help to associate animals to picture and put label on it.
</p>

<h2>Dependencies</h2>
<p>
python3 <br/>
python3 module: flask<br/>
python3 module: pillow<br/>
</p>
<h2>Shortcut</h2>
<h3>Shortcut</h3>
<p>
w: save and go back<br/>
d: check<br/>
a: uncheck<br/>
<p>

z: enable/disable zoom
</p>


<h2>Initialization</h2>

<h3>Config</h3>
open config.py <br/>
in the photo variable,put the path to the photos folder<br/>
The photo folder must contain subfolders whose name is the camera name<br/>
each subfolder contain pictures taken by its camera

<h3>species attributs</h3>
open the especes.py file
folow the instruction in the file to define species attributs

<h3>First launch</h3>
launch identification_chevreuil.py with python3<br/>
it create a database (chevreuil.db) where the data will be stored (it take some time if there is a lot of photos)<br/>
You can copy the database for backup propose<br/>
If you displace or delete the database, the software will do the Initialisation again. It is a way to start a new session.

<h2>Usage</h2>
no described yet

<h3>sort_pictures.py</h3>
if you launch this script, it will create a folder of camera where the animals ar sorted in subfolders.

<h3>convert_event_to_excsl2.R</h3>
create a excel sheet and a csv sheet with each event, it date and it description.
Not finished
