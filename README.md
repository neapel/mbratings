MusicBrainz ratings synchroinsation
===================================

This is a python plugin for [Rhythmbox](http://www.rhythmbox.org/) to automatically synchronise the ratings from your library to your [musicbrainz.org](http://musicbrainz.org)-account. They will be visible on your [user profile](http://musicbrainz.org/user/ratings/).

Requires the `musicbrainz2` python module.

You must have used a [MusicBrainz tagger](http://musicbrainz.org/doc/Products) which adds the track-UUID as metadata to your audio files for this to work. "Rated tracks" in the settings counts the number of UUID'd tracks that were submitted, "untagged tracks" is the number of unrecognized tracks. (I might add an option to list these tracks later…)


### Installation

On Ubuntu execute
    sudo apt-get install python-musicbrainz2
    cd ~/.local/share/rhythmbox/
    mkdir plugins ; cd plugins
    git clone git://github.com/funkycoder/mbratings.git
and restart Rhythmbox

If you run into problems start as `rhythmbox -D ratings` for debug output.


Since there is currently no sane way to retrieve the ratings from a musicbrainz.org-account, it syncs one way only. The DBM-file `~/.local/share/rhythmbox/mbratings.remote` stores the ratings that were sent to musicbrainz. Delete this file and the plugin will send all the ratings again (for example when choosing a different user).

Your password will be stored unencrypted in gconf (like the last.fm plugin does)
