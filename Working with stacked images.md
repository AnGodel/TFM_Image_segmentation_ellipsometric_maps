# Working with stacked images

The maps naming convention is different depending on the grabbing method:

- Maps obtained with traditional nulling method will be named with just a rolling number at the end (xxx_001.png, xxx_002.png, etc)
  - Not possible to distinguish delta maps from psi maps just from the file name.
  - Typically the even numbers will be delta maps and the odd numbers will be psi maps.

- Maps obtained with RCE method will be named as xxx_Delta_001.png, xxx_Psi_001.png, xxx_Delta_002.png, xxx_Psi_002.png
  - Much easier to handle, but the preprocessing algorithm must be different.