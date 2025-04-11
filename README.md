# mseedHeli

Create monitoring plots from miniseed data using *obspy*.

Some scripts work on all miniseed files in the current directory.

Use the following command example to copy miniseed files to the current directory.
```
find /mnt/mvohvs3/MVOSeisD6/mseed/MV -type f -name '2023.109.*Z.mseed' -print0 | xargs -0 cp --target-directory=.
```

The filenames of the plots are the same as those created by *earthworm*, but with an 'a' at the end. They can be moved to the folders in */mnt/mvofls2/Seismic_Data/monitoring_data*.

## mseedHeli.py

* Creates helicorder plots.
* Works on all miniseed files in the current directory.

## mseedSgram.py

* Creates spectrograms.
* Works on all miniseed files in the current directory.
* Under development. Plot size and Z scale need changing.

## mseedHeliNoFrills, mseedHeliNoFrillsFiles.py, mseedHeliNoFrills.py

* Creates helicorder plots with no annotation and cropped tightly.
* Saves plots in /mnt/mvofls2/Seismic_Data/monitoring_data/helicorder_plots_raw*.
* Experimental script, not implemented in routine processing.

## tidyMseedFiles.sh

* Deletes some miniseed files in current directory.

## Author

Roderick Stewart, Dormant Services Ltd

rod@dormant.org

https://services.dormant.org/

## Version History

* 1.0-dev
    * Working version

## License

This project is the property of Montserrat Volcano Observatory.
