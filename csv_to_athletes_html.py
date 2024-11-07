import csv
import re
import os

def generate_html_links(directory):
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    
    nav_content = '''<details>
      <summary>MEN's TEAM</summary>
    '''
    for html_file in html_files:
        formatted_file_name = re.split('\d+', html_file)
        nav_content += f'  <a href="{html_file}">{formatted_file_name[0:-1][0]}</a><br>\n'
    nav_content += '</details>'
    
    return nav_content

def process_athlete_data(file_path):

   # Extracting athlete stats by year
   records = []

   # Extracting athlete races
   races = []           

   athlete_name = ""
   athlete_id = ""
   comments = ""

   with open(file_path, newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      data = list(reader)

      athlete_name = data[0][0]
      athlete_id = data[1][0]
      print(f"The athlete id for {athlete_name} is {athlete_id}")

      for row in data[5:-1]:
         if row[2]:
            records.append({"year": row[2], "sr": row[3]})
         else:
            races.append({
               "finish": row[1],
               "time": row[3],
               "meet": row[5],
               "url": row[6],
               "comments": row[7]
            })

   return {
      "name": athlete_name,
      "athlete_id": athlete_id,
      "season_records": records,
      "race_results": races,
      "comments": comments
   }    

def gen_athlete_page(data, outfile):
   # template 
   # Start building the HTML structure
   current_directory = os.getcwd()+ "/mens_team"
   print(f'dir={current_directory}')
   nav_html = generate_html_links(current_directory)
   html_content = f'''<!DOCTYPE html>
   <html lang="en">
   <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
       
      <link rel = "stylesheet" href = "../css/reset.css">
      <link rel="stylesheet" href="../dist/css/lightbox.css">
      <link rel = "stylesheet" href = "../css/style.css">
      

      <title>{data["name"]}</title>
   </head>
   <body>
   <header>
      <nav>
        <ul>
            <li><a href="../index.html">Homepage</a></li>
            <li> {nav_html} </li>
             <li><a href = "https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline page</a></li>
           
        </ul>
    </nav>
    <a href="#main-content" class="skip-link">Skip to main content</a>
   
    
      <!--Athlete would input headshot-->
       <h1>{data["name"]}</h1>
       <a href="../images/profiles/{data["athlete_id"]}.jpg" data-lightbox="Athlete headshot">
         <img src="../images/profiles/{data["athlete_id"]}.jpg" alt="Athlete headshot" width="200"> 
       </a>
       <!-- Dark Mode Toggle Switch -->
    
   </header>
   <main id = "main-content">
      <h2>Athlete's Summary</h2>
      <section id= "athlete-sr-table">
            <table>
                  <thead>
                     <tr>
                        <th> Year </th>
                        <th> Season Record (SR)</th>
                     </tr>
                  </thead>
                  <tbody>
                  '''
   
   for sr in data["season_records"]:
      sr_row = f'''
                     <tr>
                        <td>{sr["year"]}</td>
                        <td>{sr["sr"]}</td>
                     </tr>                  
               '''
      html_content += sr_row

   html_content += '''                   
                </tbody>
                  </table>
                     </section>

                        <h2>Race Results</h2>

                        <section id="athlete-result-table">
                           

                           <table id="athlete-table">
                              <thead>
                                 <tr>
                                    <th>Race</th>
                                    <th>Athlete Time</th>
                                    <th>Athlete Place</th>
                                    <th>Race Comments</th>
                                 </tr>
                              </thead>

                              <tbody>
                  '''

   # add each race as a row into the race table 
   for race in data["race_results"]:
      race_row = f'''
                                 <tr class="result-row">
                                    <td>
                                       <a href="{race["url"]}">{race["meet"]}</a>
                                    </td>
                                    <td>{race["time"]}</td>
                                    <td>{race["finish"]}</td>
                                     <td>{race["comments"]}</td>
                                 </tr>
      '''
      html_content += race_row

   html_content += '''
                              </tbody>

                        </table>
                     </section>

                     </main>
                     <footer>
                     <p>
                     Skyline High School<br>
                     <address>
                     2552 North Maple Road<br>
                     Ann Arbor, MI 48103<br><br>

                     
                    <a href = "https://www.instagram.com/a2skylinexc/">Follow us on instagram</a> 

                     </footer>
<script>
console.log('here')
// Select all images on the page
document.querySelectorAll('img').forEach(img => {
  img.onerror = function() {
   
    this.onerror = null; // Prevents infinite loop if default image missing
    this.src = '../images/profiles/default.jpg';
    this.alt = ""
    console.log("image is "+this.src)
  };
});  
</script> 
                     
                                       
                                                                           <script>
    document.addEventListener('DOMContentLoaded', function () {
        const toggleSwitch = document.getElementById('dark-mode-toggle');

        // Initialize theme
        const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;
        if (currentTheme) {
            document.body.setAttribute('data-theme', currentTheme);
            if (currentTheme === 'dark') {
                toggleSwitch.checked = true;
            }
        }

        // Toggle theme on switch change
        // toggleSwitch.addEventListener('change', function() {
            if (this.checked) {
                document.body.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.removeAttribute('data-theme');
                localStorage.setItem('theme', 'light');
            }
        });
    
</script>
<script 
   src="../dist/js/lightbox-plus-jquery.js">
</script>

               
               </body>
         </html>
   '''

   with open(outfile, 'w') as output:
      output.write(html_content)


def main():

   import os
   import glob

   # Define the folder path
   folder_path = 'mens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("mens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "mens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")


   # Define the folder path
   folder_path = 'womens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("womens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "womens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")

if __name__ == '__main__':
    main()
