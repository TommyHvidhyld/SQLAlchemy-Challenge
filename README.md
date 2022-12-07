# SQLAlchemy-Challenge
Climate Analysis of Hawaii using SQLAlchemy
To help with trip planning to Hawaii, I did a climate analysis about the area using a sqlite file containing weather information. Specifically I used SQLAlchemy ORM queries, Pandas, and Matplotlib to complete the analysis.

Part one included analyzing and exploring the climate data. The percipitation analysis involved querying the previous twelve monthes of data and putting it into a dataframe. From there created a bar chart showing the information using Matplotlib. As well as providing summary statistics of the precipitation data. Next was the station analysis. Station being where the temperature observations and percipitation data was recorded. Queries were made to find the most-active station and then calculating the lowest, highest, and average temperatures of the specified station. A histogram was used to present this data.

Part two was designing a climate app for the data. By designing a flask API based on the queries developed in part one, users would be able to find specific precipitation, station, temperature, and specific dates of temperature data. The app was designed in VScode, and ran properly based on user input.
