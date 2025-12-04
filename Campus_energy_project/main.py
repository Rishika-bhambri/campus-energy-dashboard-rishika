import os
import pandas as pd
import matplotlib.pyplot as plt  # Graph banane ke liye

# --- TASK 3: OOP Classes (Saanche) ---

class MeterReading:
    """Yeh class ek single bijli ki reading store karegi"""
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    """Yeh class puri Building ka data manage karegi"""
    def __init__(self, name):
        self.name = name
        self.readings = []  # Is list mein saari readings ayengi

    def add_reading(self, reading_obj):
        """Reading ko list mein add karne ka function"""
        self.readings.append(reading_obj)

    def calculate_total_consumption(self):
        """Saari readings ka total jod kar batayega"""
        total = 0
        for reading in self.readings:
            total += reading.kwh
        return total

# 1. Folder ka rasta set karte hain
folder_path = 'data/'  # Make sure tera folder name yahi ho
all_building_data = [] # Khali list jisme saara data jama karenge

print("Data load karna shuru kar rahe hain...")

# 2. Folder ke har file ko check karte hain [cite: 6]
try:
    files = os.listdir(folder_path)
    
    for filename in files:
        # Sirf CSV files chahiye
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            
            # 3. CSV ko padhte hain [cite: 7, 8]
            try:
                # 'on_bad_lines' corrupt data ko handle karega [cite: 8]
                df_temp = pd.read_csv(file_path, on_bad_lines='skip')
                
                # Filename se building ka naam nikal kar column mein daal rahe hain
                building_name = filename.replace('.csv', '')
                df_temp['Building_Name'] = building_name
                
                # List mein add kar diya
                all_building_data.append(df_temp)
                print(f"Successfully loaded: {filename}")
                
            except Exception as e:
                print(f"Error reading {filename}: {e}")

    # 4. Saare tukdon ko ek bade table mein jodna [cite: 9]
    if all_building_data:
        final_df = pd.concat(all_building_data, ignore_index=True)
        print("\n--- Summary ---")
        print("Total Files Loaded:", len(all_building_data))
        print("Combined Data Shape:", final_df.shape)
        print("\nFirst 5 rows:")
        print(final_df.head())
    else:
        print("Koi CSV file nahi mili! Check karo 'data' folder sahi jagah hai ya nahi.")

except FileNotFoundError:
    print(f"Folder '{folder_path}' nahi mila. Please check karo folder create kiya hai ya nahi.")
    # ... Upar wala code waisa hi rahega ...

# Agar data load hua hai tabhi aage badhenge
if 'final_df' in locals() and not final_df.empty:
    
    print("\n--- Task 2: Statistics & Calculation ---")

    # Step A: Date wale column ko sahi format mein convert karna
    # Yeh zaroori hai, nahi toh 'resample' kaam nahi karega
    final_df['Timestamp'] = pd.to_datetime(final_df['Timestamp'])

    # Step B: Daily Totals Nikalna (Har din ka total consumption)
    # Pehle Timestamp ko index banate hain
    df_indexed = final_df.set_index('Timestamp')
    
    # 'D' matlab Daily. Hum KWh_usage ka sum kar rahe hain.
    daily_totals = df_indexed['KWh_usage'].resample('D').sum()
    
    print("\nDaily Energy Consumption:")
    print(daily_totals)

    # Step C: Building-wise Summary
    # Har building ka Average, Min, Max aur Total ek saath nikalenge
    summary_table = final_df.groupby('Building_Name')['KWh_usage'].agg(['mean', 'min', 'max', 'sum'])
    
    print("\nBuilding Performance Summary:")
    print(summary_table)

    # (Optional) Is summary ko CSV mein save kar lete hain (Task 5 ka part)
    summary_table.to_csv('output/building_summary.csv')
    print("\nSummary saved to 'output/building_summary.csv'")

else:
    print("Data load nahi hua, isliye calculation skip kar rahe hain.")
    # ... Upar wala code waisa hi rahega ...

if 'final_df' in locals() and not final_df.empty:
    
    print("\n--- Task 3: OOP Processing ---")
    
    # Ek dictionary banayenge saari buildings ko store karne ke liye
    campus_buildings = {} 

    # DataFrame ki har row par loop chalayenge
    # Yeh thoda time le sakta hai agar data bahut zyada ho
    for index, row in final_df.iterrows():
        b_name = row['Building_Name']
        time = row['Timestamp']
        usage = row['KWh_usage']
        
        # 1. Check karo: Kya yeh building pehle se hamari list mein hai?
        if b_name not in campus_buildings:
            # Agar nahi, toh nayi Building create karo
            campus_buildings[b_name] = Building(b_name)
        
        # 2. Reading ka object banao
        reading = MeterReading(time, usage)
        
        # 3. Building ke andar reading add karo
        campus_buildings[b_name].add_reading(reading)

    print("OOP Objects create ho gaye!")
    
    # Test karte hain: Har building ka total print karte hain OOP use karke
    print("\nOOP Calculated Totals:")
    for name, building_obj in campus_buildings.items():
        total = building_obj.calculate_total_consumption()
        print(f"Building: {name}, Total: {total:.2f} kWh")

else:
    print("Data load nahi hua, OOP step skip kar rahe hain.")
    # ... Upar wala OOP code waisa hi rahega ...

if 'final_df' in locals() and not final_df.empty:

    print("\n--- Task 4: Visualization (Graphs) ---")
    
    # 3 Graphs ke liye jagah bana rahe hain (3 rows, 1 column)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))
    fig.suptitle('Campus Energy Consumption Dashboard', fontsize=16)

    # Graph 1: Trend Line (Daily Totals)
    # Humne Task 2 mein 'daily_totals' nikala tha, wahi use karenge
    ax1.plot(daily_totals.index, daily_totals.values, marker='o', linestyle='-', color='b')
    ax1.set_title('Daily Total Consumption Trend')
    ax1.set_ylabel('kWh Usage')
    ax1.grid(True)

    # Graph 2: Bar Chart (Building-wise Average)
    # Task 2 wala 'summary_table' use karenge
    buildings = summary_table.index
    avg_usage = summary_table['mean']
    ax2.bar(buildings, avg_usage, color='green')
    ax2.set_title('Average Consumption per Building')
    ax2.set_ylabel('Average kWh')

    # Graph 3: Scatter Plot (Peak Hours)
    # Pehle hum check karenge kis ghante (hour) mein kitni bijli jali
    final_df['Hour'] = final_df['Timestamp'].dt.hour
    ax3.scatter(final_df['Hour'], final_df['KWh_usage'], alpha=0.5, color='red')
    ax3.set_title('Consumption vs. Hour of Day (Peak Load Analysis)')
    ax3.set_xlabel('Hour of Day (0-23)')
    ax3.set_ylabel('kWh Usage')
    ax3.grid(True)

    # Graph ko save karna
    plt.tight_layout()
    plt.savefig('output/dashboard.png')
    print("Graph saved: output/dashboard.png")

    print("\n--- Task 5: Reports & Export ---")

    # 1. Cleaned Data Export
    final_df.to_csv('output/cleaned_energy_data.csv', index=False)
    print("Data saved: output/cleaned_energy_data.csv")

    # 2. Text Summary Report
    # Sabse zyada bill kiska aaya? (Max consumption building)
    max_building = summary_table['sum'].idxmax()
    max_value = summary_table['sum'].max()
    total_campus_usage = final_df['KWh_usage'].sum()

    with open('output/summary.txt', 'w') as f:
        f.write("--- CAMPUS ENERGY EXECUTIVE SUMMARY ---\n")
        f.write(f"Total Campus Consumption: {total_campus_usage:.2f} kWh\n")
        f.write(f"Highest Consuming Building: {max_building} ({max_value:.2f} kWh)\n")
        f.write("\nBuilding-wise Breakdown:\n")
        f.write(summary_table.to_string())
    
    print("Report saved: output/summary.txt")
    print("\n✅ PROJECT COMPLETE! Saare tasks ho gaye.")

else:
    print("Data nahi hai, graphs nahi ban sakte.")