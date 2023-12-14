Project **"Air Quality Monitoring"**
Project Overview
This project focuses on gathering and processing air quality data from stations operated by the Executive Environmental Agency (IAOS) into a database. The implemented scraper code downloads data from the IAOS platform for each air quality factor (e.g., temperature, NO2, etc.) separately for the previous day. The collected data is then aggregated into a CSV file for each element. The code handles data from five stations (Sofia, Pavlovo, Hipodruma, Druzhba, Mladost). It accounts for the temporal characteristics of the data, automatically filling missing entries with predefined values.

The method employed involves filtering the data for each element, storing it for the previous day, as the IAOS platform provides unnecessary data for each element. The method uploads the collected data to a specified Postgres database, with maximum automation and notification functions for events such as successful data recording, errors, etc.

After gathering data into the database, an API was developed to query and retrieve information about air quality. The API provides capabilities to extract data based on various air quality factors, such as temperature and NO2. Additionally, efforts were made to enhance the visualization of this data. The heatmap, a previous student's thesis project, visually represents air quality in different regions. Through colors and their intensity, pollution levels in various parts of the region can be easily discerned.

Project Architecture
Backend
The backend part is hosted on a Tomcat server responsible for storing and managing data collected from the Flask API and other components of the backend system.

Frontend
The frontend part, representing the heatmap, is deployed on an IIS server (Internet Information Services). This component does not contain data but visualizes air quality graphically, providing a visual interface accessible through web browsers.

Reverse Proxy
A second website was created on the IIS server with a reverse proxy, redirecting requests to the Tomcat server with backend data. This enables the frontend to make requests outside the virtual machine. 

Currently, the heatmap uses demo data. Users can access the heatmap through web browsers at the following address: https://twin-web.gate-ai.eu/.
