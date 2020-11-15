# What does each notebook do?

## oakland_only.ipynb
 - Very first notebook doing early exploration on datasets
 - This notebook really was only for early testing of AutoML and jupyter

## all_zones_occupancy.ipynb (milestone 1)
 - This notebook calculates occuapncy for every zone in the city of Pittsburgh
 - It does not use meter values, instead it uses zone aggregates of the time buckets
 	- This approach was abandoned early in developmenet, so it's safe to disregard.
 - In previous versions, there were notebooks for cleaning up errors, they are also not neccesary
 - The procedure in this notebook was originally done on just Oakland data in generate_true_free_spaces.ipynb, which is also not neccesary

## meter_occupancy.ipynb (milestone 2/3)
 - This notebook (tediously) calcualtes occupancy for every meter in the city.
 	- Mobile occuapncies are generated on a zone-by-zone basis; we created these for just Oakland zones, but you can change it to be any zone by editing the OAKLAND_1 variable
 		- To generate the mobile csv's, we take the ratio of physical meter transactions to physical zone transactions and apply that same ratio to solve for virtual meter transactions given virtual meter transactions
 		- Mobile occupancies are used in milestone 3
 - Requires /data/meters.csv and 2018--transactions.csv which can be found here (https://data.wprdc.org/dataset/parking-purchases/resource/2bd36135-1104-4988-92c6-64a43ffbdf0d )
 - While this notebook has gone through several speed improvements, runtime is still several hours.  Be sure to not let your computer go to sleep while running it

## milestone_2.ipynb
 - This notebook gathers the oakland meters to generate a single training csv for the model oakland_meter_nonmobile_data
 - Requires having generated meter csv's for all Oakland meters

## milestone_3.ipynb
 - This notebook creates several csv's for training using meter csvs INCLUDING mobile data
 - We estimate capacity of a meter (total spaces) by taking the 90'th quantile of used spaces across the entire year of a particular meter
 	- 90 was reasonably arbitrary, though among tetsed values, it lead to the best looking distribution.
 - We generate three csv's
 	- 1: all buckets in a year for all meters in oakland (OAKLAND_with_mobile_occupancies.csv)
 		- model is called oakland_meter_mobile_included
 	- 2: only buckets within "business hours" of 6am to 6pm (OAKLAND_6am_to_6pm_occupancies.csv)
 		- The graphs from this creation was not distinct enough from the csv of all buckets, so no model came from this
 	- 3: csv removing all buckets with occuapncy of zero (OAKLAND_non_zero_buckets.csv)
 		- model is called oakland_non_zero_buckets
 - We also compare the non mobile model from Mileston 2 with the two models from this milestone in boxplots to see which one best fits the calculation for occupancy
 	- Note that since the non-mobile model does not factor in mobile transations, it should be an underestimate.  It has a wider spread however, which leads us to believe it is the worst model.