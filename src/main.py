import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from pathlib import Path
from datetime import datetime
import glob

# ============================================================================
# IMAGE PROCESSING CONFIGURATION
# ============================================================================

# HSV ranges for triglycerides (yellow)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([35, 255, 255])

def calculate_lipid_percentage(image):
    """Calculates the percentage of triglyceride pixels"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Dilate to capture edges
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30))
    mask_dilated = cv2.dilate(mask, kernel, iterations=1)
    
    percentage = np.sum(mask_dilated > 0) / mask_dilated.size * 100
    return percentage, mask_dilated

def process_and_save_image(image, mask, base_name, results_folder):
    """Processes and saves resulting images"""
    os.makedirs(results_folder, exist_ok=True)
    
    # 1. Fused image (original + magenta)
    magenta = np.zeros_like(image)
    magenta[:] = (255, 0, 255)  # Magenta in BGR
    magenta_highlight = cv2.bitwise_and(magenta, magenta, mask=mask)
    fused = cv2.addWeighted(image, 1.0, magenta_highlight, 0.5, 0)
    
    # 2. Combined image (original | processed)
    combined = np.hstack((image, fused))
    cv2.putText(combined, base_name, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Save images
    fused_path = os.path.join(results_folder, f"fused_{base_name}")
    combined_path = os.path.join(results_folder, f"comparison_{base_name}")
    
    cv2.imwrite(fused_path, fused)
    cv2.imwrite(combined_path, combined)
    
    return fused_path, combined_path

# ============================================================================
# MAIN SYSTEM - SIMPLIFIED
# ============================================================================

class CellCultureAnalysisSystem:
    def __init__(self):
        """Initializes the simplified system"""
        self.data = {
            'experiment_name': '',
            'culture_type': '',
            'days': [],  # List of analyzed days
            'images_per_day': {},  # {day: [list_of_image_paths]}
            'results_per_day': {},  # {day: [list_of_percentages]}
            'processed_paths': {}  # {day: {idx: (fused_path, comparison_path)}}
        }
    
    def show_header(self):
        """Displays system header"""
        # ANSI color codes
        BLUE = "\033[94m"
        GREEN = "\033[92m"
        GOLD = "\033[93m"
        RESET = "\033[0m"
        
        logo = f"""
    {BLUE}         ╭─────────────────────────╮{RESET}
    {BLUE}         │     ○            ○      │{RESET}
    {BLUE}         │    ○  \\        / ○      │{RESET}
    {BLUE}         │  {GOLD}.{BLUE}  \\  ○ {GOLD} ◉{BLUE}   ○ /   {GOLD}.{BLUE}   │{RESET}
    {BLUE}         │      ○  \\    / ○        │{RESET}
    {BLUE}         │  {GOLD} ●{BLUE}  |   ○  ○  |  {GOLD}●{BLUE}     │{RESET}
    {BLUE}         │      ○   |  |  ○        │{RESET}
    {BLUE}         │ {GOLD}◉{BLUE}   /    ○   ○  \\ {GOLD} ◉{BLUE}    │{RESET}
    {BLUE}         │   ○    /      \\  ○      │{RESET}
    {BLUE}         │       ○        ○        │{RESET}
    {BLUE}         │         IPICYT          │{RESET}  
    {BLUE}         │    {GOLD}25 Aniversario{BLUE}       │{RESET}
    {BLUE}         ╰─────────────────────────╯{RESET}
        """
        print(logo)
        print("="*90)
        print("Welcome to the Triglyceride Localization via Edge-Triggered Segmentation system \n")
        print("="*90)
    
    # ============================================================================
    # STEP 1: BASIC INFORMATION
    # ============================================================================
    
    def step1_basic_information(self):
        """Step 1: Requests basic information"""
        print("\n📋 BASIC INFORMATION")
        print("-"*40)
        
        self.data['experiment_name'] = input("Experiment name: ").strip()
        while not self.data['experiment_name']:
            print("❌ Name is required")
            self.data['experiment_name'] = input("Experiment name: ").strip()
        
        self.data['culture_type'] = input("Culture type: ").strip()
        if not self.data['culture_type']:
            self.data['culture_type'] = "Unnamed culture"
        
        print(f"\n✅ Experiment: {self.data['experiment_name']}")
        print(f"✅ Culture: {self.data['culture_type']}")
    
    # ============================================================================
    # STEP 2: PROCESS BY DAYS
    # ============================================================================
    
    def step2_process_by_days(self):
        """Step 2: Processes each day sequentially"""
        print("\n" + "="*60)
        print(" PROCESSING BY DAYS")
        print("="*60)
        
        day_number = 1
        
        while True:
            print(f"\n📅 DAY {day_number}")
            print("-"*30)
            
            day_input = input("Enter day number (e.g., 0, 1, 2, 3) or 'q' to finish: ").strip()
            
            if day_input.lower() == 'q':
                if day_number == 1:
                    print("⚠️ You must enter at least one day")
                    continue
                break
            
            try:
                day = float(day_input)
                
                if day in self.data['days']:
                    print(f"⚠️ Day {day} is already registered")
                    continue
                
                print(f"\n📸 UPLOADING IMAGES FOR DAY {day}")
                print("-"*40)
                
                # Process images for this day
                image_paths = self._upload_images_for_day(day)
                
                if image_paths:
                    self.data['days'].append(day)
                    self.data['images_per_day'][day] = image_paths
                    self.data['results_per_day'][day] = []
                    self.data['processed_paths'][day] = {}
                    
                    print(f"✅ Day {day}: {len(image_paths)} images registered")
                    day_number += 1
                else:
                    print(f"❌ No images registered for day {day}")
                    
            except ValueError:
                print("❌ Error: Enter a valid number")
    
    def _upload_images_for_day(self, day):
        """Uploads images for a specific day"""
        image_paths = []
        image_num = 1
        
        print("\nHow do you want to upload images?")
        print("1. Select individual images")
        print("2. Select a folder with images")
        
        while True:
            option = input("\nOption (1/2): ").strip()
            
            if option == '1':
                return self._upload_individual_images(day)
            elif option == '2':
                return self._upload_images_from_folder(day)
            else:
                print("❌ Invalid option. Try again.")
    
    def _upload_individual_images(self, day):
        """Uploads images one by one"""
        paths = []
        print("\n📁 UPLOADING INDIVIDUAL IMAGES")
        print("Enter the path of each image")
        print("Enter 'q' when finished")
        print("-"*40)
        
        while True:
            print(f"\nImage #{len(paths) + 1}")
            path = input("Image path (or 'q' to finish): ").strip()
            
            if path.lower() == 'q':
                if len(paths) == 0:
                    print("⚠️ You must enter at least one image")
                    continue
                break
            
            path = path.replace("\\", "/").strip('"').strip("'")
            
            if not os.path.exists(path):
                print("❌ Path does not exist")
                continue
            
            # Verify it's an image
            extensions = ('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp', '.gif')
            if not path.lower().endswith(extensions):
                print("⚠️ The file doesn't seem to be an image")
                continue_option = input("Continue anyway? (y/n): ").lower()
                if continue_option != 'y':
                    continue
            
            paths.append(path)
            print(f"✅ Image {len(paths)} added: {os.path.basename(path)}")
        
        return paths
    
    def _upload_images_from_folder(self, day):
        """Uploads ALL images from a folder"""
        print("\n📁 UPLOADING ALL IMAGES FROM A FOLDER")
        print("-"*40)
        
        while True:
            folder_path = input("Folder path: ").strip()
            folder_path = folder_path.replace("\\", "/").strip('"').strip("'")
            
            if not os.path.exists(folder_path):
                print("❌ Folder does not exist")
                continue
            
            # Find ALL images in the folder
            extensions = ['*.png', '*.jpg', '*.jpeg', '*.tif', '*.tiff', '*.bmp', '*.gif',
                         '*.PNG', '*.JPG', '*.JPEG', '*.TIF', '*.TIFF', '*.BMP', '*.GIF']
            
            image_paths = []
            for ext in extensions:
                pattern = os.path.join(folder_path, ext)
                image_paths.extend(glob.glob(pattern))
            
            # Sort by name for consistency
            image_paths.sort()
            
            if not image_paths:
                print("❌ No images found in the folder")
                continue
            
            print(f"\n✅ Found {len(image_paths)} images:")
            for i, path in enumerate(image_paths[:10], 1):  # Show first 10
                print(f"  {i}. {os.path.basename(path)}")
            
            if len(image_paths) > 10:
                print(f"  ... and {len(image_paths)-10} more")
            
            confirm = input(f"\nProcess all {len(image_paths)} images? (y/n): ").lower()
            if confirm == 'y':
                return image_paths
            else:
                print("❌ Canceled. Try with another folder.")
    
    # ============================================================================
    # STEP 3: PROCESS ALL IMAGES
    # ============================================================================
    
    def step3_process_images(self):
        """Step 3: Processes all uploaded images"""
        print("\n" + "="*60)
        print(" PROCESSING IMAGES")
        print("="*60)
        
        # Create main results folder
        base_name = self.data['experiment_name'].replace(' ', '_')
        base_folder = f"Results_{base_name}"
        os.makedirs(base_folder, exist_ok=True)
        
        total_images = sum(len(imgs) for imgs in self.data['images_per_day'].values())
        print(f"🔬 Processing {total_images} images...")
        
        for day in sorted(self.data['days']):
            print(f"\n📊 DAY {day}:")
            
            # Folder for this day
            day_folder = os.path.join(base_folder, f"Day_{day}")
            os.makedirs(day_folder, exist_ok=True)
            
            day_results = []
            self.data['processed_paths'][day] = {}
            
            for idx, image_path in enumerate(self.data['images_per_day'][day], 1):
                print(f"  Image {idx}/{len(self.data['images_per_day'][day])}: ", end="")
                
                # Load image
                image = cv2.imread(image_path)
                if image is None:
                    print(f"❌ Error loading {os.path.basename(image_path)}")
                    day_results.append(0)  # Default value if error
                    continue
                
                # Calculate lipid percentage
                percentage, mask = calculate_lipid_percentage(image)
                day_results.append(percentage)
                
                # Process and save images
                base_img_name = f"Day{day}_Img{idx}_{os.path.basename(image_path)}"
                fused_path, comparison_path = process_and_save_image(
                    image, mask, base_img_name, day_folder
                )
                
                # Save paths
                self.data['processed_paths'][day][idx] = {
                    'fused': fused_path,
                    'comparison': comparison_path,
                    'original': image_path,
                    'percentage': percentage
                }
                
                print(f"{percentage:.2f}% lipids ✓")
            
            # Save day results
            self.data['results_per_day'][day] = day_results
        
        print(f"\n✅ Processing completed")
        print(f"📁 Results in: {base_folder}/")
        return base_folder
    
    # ============================================================================
    # STEP 4: STATISTICAL ANALYSIS
    # ============================================================================
    
    def step4_statistical_analysis(self):
        """Step 4: Performs statistical analysis"""
        print("\n" + "="*60)
        print(" STATISTICAL ANALYSIS")
        print("="*60)
        
        if not self.data['results_per_day']:
            print("❌ No results to analyze")
            return None
        
        statistical_results = {
            'days': [],
            'averages': [],
            'standard_deviations': [],
            'standard_errors': [],
            'error_margins': [],
            'num_images': [],
            'minimums': [],
            'maximums': []
        }
        
        print("\n📈 RESULTS BY DAY:")
        print("-"*50)
        
        for day in sorted(self.data['days']):
            values = self.data['results_per_day'][day]
            
            if values:
                average = np.mean(values)
                std_dev = np.std(values, ddof=1) if len(values) > 1 else 0
                std_error = std_dev / np.sqrt(len(values))
                error_margin = 1.96 * std_error  # 95% CI
                minimum = np.min(values)
                maximum = np.max(values)
                
                statistical_results['days'].append(day)
                statistical_results['averages'].append(average)
                statistical_results['standard_deviations'].append(std_dev)
                statistical_results['standard_errors'].append(std_error)
                statistical_results['error_margins'].append(error_margin)
                statistical_results['num_images'].append(len(values))
                statistical_results['minimums'].append(minimum)
                statistical_results['maximums'].append(maximum)
                
                print(f"\n📊 DAY {day}:")
                print(f"  Images: {len(values)}")
                print(f"  Average: {average:.2f}%")
                print(f"  Range: {minimum:.2f}% - {maximum:.2f}%")
                print(f"  Error margin (95%): ±{error_margin:.2f}%")
                
                # Show some individual values
                if len(values) <= 10:
                    for i, value in enumerate(values, 1):
                        print(f"    Image {i}: {value:.2f}%")
                else:
                    print(f"    First image: {values[0]:.2f}%")
                    print(f"    Last image: {values[-1]:.2f}%")
                    print(f"    Median: {np.median(values):.2f}%")
        
        return statistical_results
    
    # ============================================================================
    # STEP 5: GENERATE GRAPHS
    # ============================================================================
    
    def step5_generate_graphs(self, results, base_folder):
        """Step 5: Generates result graphs"""
        print("\n" + "="*60)
        print(" GENERATING GRAPHS")
        print("="*60)
        
        if not results or not results['days']:
            print("❌ No data to graph")
            return []
        
        graph_files = []
        
        # ============================================
        # GRAPH 1: Temporal evolution
        # ============================================
        plt.figure(figsize=(12, 7))
        
        # Main line with error bars
        plt.errorbar(
            results['days'],
            results['averages'],
            yerr=results['error_margins'],
            fmt='o-',
            capsize=8,
            linewidth=3,
            markersize=10,
            color='navy',
            label='Average ± 95% CI',
            alpha=0.8
        )
        
        # Hat to show range (minimum-maximum)
        for i, day in enumerate(results['days']):
            plt.plot([day, day], 
                    [results['minimums'][i], results['maximums'][i]], 
                    color='red', alpha=0.3, linewidth=2)
        
        # Configuration
        plt.title(f'Lipid Evolution\n{self.data["culture_type"]} - {self.data["experiment_name"]}',
                 fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Days in Culture', fontsize=12, labelpad=10)
        plt.ylabel('Lipid Percentage (%)', fontsize=12, labelpad=10)
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.legend()
        
        # Adjust limits
        if results['days']:
            plt.xlim(min(results['days']) - 0.5, max(results['days']) + 0.5)
            y_max = max(results['maximums']) * 1.2 if results['maximums'] else 50
            plt.ylim(0, y_max)
        
        plt.tight_layout()
        
        # Save
        graph1_name = os.path.join(base_folder, "Graph_Evolution.png")
        plt.savefig(graph1_name, dpi=300, bbox_inches='tight')
        graph_files.append(graph1_name)
        print(f"✅ Graph 1: Temporal evolution saved")
        
        # ============================================
        # GRAPH 2: Distribution by day (boxplot)
        # ============================================
        if len(results['days']) > 1:
            plt.figure(figsize=(10, 6))
            
            # Prepare data for boxplot
            boxplot_data = []
            labels = []
            
            for day in sorted(self.data['days']):
                values = self.data['results_per_day'][day]
                if values:
                    boxplot_data.append(values)
                    labels.append(f'Day {day}')
            
            # Create boxplot
            box = plt.boxplot(boxplot_data, labels=labels, patch_artist=True)
            
            # Color the boxes
            colors = plt.cm.Set3(np.linspace(0, 1, len(boxplot_data)))
            for patch, color in zip(box['boxes'], colors):
                patch.set_facecolor(color)
            
            # Add individual points
            for i, values in enumerate(boxplot_data, 1):
                x = np.random.normal(i, 0.04, size=len(values))
                plt.scatter(x, values, alpha=0.6, s=30, color='black', 
                           edgecolors='white', linewidth=0.5)
            
            # Configuration
            plt.title(f'Distribution by Day\n{self.data["culture_type"]} - {self.data["experiment_name"]}',
                     fontsize=14, fontweight='bold')
            plt.xlabel('Day', fontsize=12)
            plt.ylabel('Lipid Percentage (%)', fontsize=12)
            plt.grid(axis='y', alpha=0.3, linestyle='--')
            plt.tight_layout()
            
            # Save
            graph2_name = os.path.join(base_folder, "Graph_Distribution.png")
            plt.savefig(graph2_name, dpi=300, bbox_inches='tight')
            graph_files.append(graph2_name)
            print(f"✅ Graph 2: Distribution by day saved")
        
        # ============================================
        # GRAPH 3: Statistical summary
        # ============================================
        plt.figure(figsize=(14, 5))
        
        # Subplot 1: Averages
        plt.subplot(1, 3, 1)
        plt.bar(range(len(results['days'])), results['averages'], 
                color='skyblue', edgecolor='black')
        plt.title('Averages by Day', fontsize=12)
        plt.xlabel('Day', fontsize=10)
        plt.ylabel('Lipids (%)', fontsize=10)
        plt.xticks(range(len(results['days'])), [f'Day {d}' for d in results['days']])
        
        # Subplot 2: Number of images
        plt.subplot(1, 3, 2)
        plt.bar(range(len(results['days'])), results['num_images'], 
                color='lightgreen', edgecolor='black')
        plt.title('Number of Images', fontsize=12)
        plt.xlabel('Day', fontsize=10)
        plt.ylabel('Quantity', fontsize=10)
        plt.xticks(range(len(results['days'])), [f'Day {d}' for d in results['days']])
        
        # Subplot 3: Range (min-max)
        plt.subplot(1, 3, 3)
        for i, day in enumerate(results['days']):
            plt.plot([i, i], [results['minimums'][i], results['maximums'][i]], 
                    'o-', color='red', linewidth=2, markersize=8)
            plt.plot(i, results['averages'][i], 's', color='blue', markersize=10)
        plt.title('Range and Average', fontsize=12)
        plt.xlabel('Day', fontsize=10)
        plt.ylabel('Lipids (%)', fontsize=10)
        plt.xticks(range(len(results['days'])), [f'Day {d}' for d in results['days']])
        
        plt.suptitle(f'Statistical Summary - {self.data["culture_type"]} - {self.data["experiment_name"]}', 
                    fontsize=14, fontweight='bold', y=1.05)
        plt.tight_layout()
        
        # Save
        graph3_name = os.path.join(base_folder, "Graph_Summary.png")
        plt.savefig(graph3_name, dpi=300, bbox_inches='tight')
        graph_files.append(graph3_name)
        print(f"✅ Graph 3: Statistical summary saved")
        
        plt.show()
        return graph_files
    
    # ============================================================================
    # STEP 6: SAVE DATA TO CSV
    # ============================================================================
    
    def step6_save_to_csv(self, results, base_folder):
        """Step 6: Saves results to CSV files"""
        print("\n" + "="*60)
        print(" EXPORTING DATA TO CSV")
        print("="*60)
        
        csv_files = []
        
        # ============================================
        # CSV 1: Detailed data (all images)
        # ============================================
        detailed_data = []
        
        for day in sorted(self.data['days']):
            for idx, image_path in enumerate(self.data['images_per_day'][day], 1):
                if idx in self.data['processed_paths'][day]:
                    data = self.data['processed_paths'][day][idx]
                    detailed_data.append({
                        'Experiment': self.data['experiment_name'],
                        'Culture': self.data['culture_type'],
                        'Day': day,
                        'Image_Number': idx,
                        'File_Name': os.path.basename(image_path),
                        'Lipid_Percentage': data['percentage'],
                        'Original_Path': image_path,
                        'Fused_Path': data['fused'],
                        'Comparison_Path': data['comparison']
                    })
        
        if detailed_data:
            df_detailed = pd.DataFrame(detailed_data)
            csv_detailed = os.path.join(base_folder, "Detailed_Data.csv")
            df_detailed.to_csv(csv_detailed, index=False, encoding='utf-8')
            csv_files.append(csv_detailed)
            print(f"✅ CSV 1: Detailed data ({len(detailed_data)} images)")
        
        # ============================================
        # CSV 2: Summary by day
        # ============================================
        if results and results['days']:
            df_summary = pd.DataFrame({
                'Day': results['days'],
                'Num_Images': results['num_images'],
                'Average_Lipids': results['averages'],
                'Standard_Deviation': results['standard_deviations'],
                'Standard_Error': results['standard_errors'],
                'Error_Margin_95%': results['error_margins'],
                'Minimum': results['minimums'],
                'Maximum': results['maximums']
            })
            
            csv_summary = os.path.join(base_folder, "Summary_By_Day.csv")
            df_summary.to_csv(csv_summary, index=False, encoding='utf-8')
            csv_files.append(csv_summary)
            print(f"✅ CSV 2: Summary by day")
        
        return csv_files
    
    # ============================================================================
    # STEP 7: CREATE REPORT
    # ============================================================================
    
    def step7_create_report(self, results, base_folder):
        """Step 7: Creates results report"""
        print("\n" + "="*60)
        print(" CREATING REPORT")
        print("="*60)
        
        # Create plain text summary file
        report_name = os.path.join(base_folder, "Analysis_Summary.txt")
        
        with open(report_name, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write(" CELL CULTURE ANALYSIS SUMMARY\n")
            f.write("="*60 + "\n\n")
            
            f.write(f"Experiment: {self.data['experiment_name']}\n")
            f.write(f"Culture Type: {self.data['culture_type']}\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Days Analyzed: {len(self.data['days'])}\n")
            
            total_images = sum(len(imgs) for imgs in self.data['images_per_day'].values())
            f.write(f"Total Images: {total_images}\n\n")
            
            f.write("="*60 + "\n")
            f.write(" RESULTS BY DAY\n")
            f.write("="*60 + "\n\n")
            
            if results and results['days']:
                for i, day in enumerate(results['days']):
                    f.write(f"Day {day}:\n")
                    f.write(f"  Images: {results['num_images'][i]}\n")
                    f.write(f"  Average: {results['averages'][i]:.2f}%\n")
                    f.write(f"  Minimum: {results['minimums'][i]:.2f}%\n")
                    f.write(f"  Maximum: {results['maximums'][i]:.2f}%\n")
                    f.write(f"  Standard Deviation: {results['standard_deviations'][i]:.2f}%\n")
                    f.write(f"  Error Margin (95%): ±{results['error_margins'][i]:.2f}%\n")
                    f.write(f"  Interval: [{results['averages'][i]-results['error_margins'][i]:.2f}%, "
                           f"{results['averages'][i]+results['error_margins'][i]:.2f}%]\n\n")
            
            f.write("="*60 + "\n")
            f.write(" GENERATED FILES\n")
            f.write("="*60 + "\n\n")
            
            f.write("1. Graphs:\n")
            f.write("   - Graph_Evolution.png: Temporal evolution\n")
            f.write("   - Graph_Distribution.png: Distribution by day\n")
            f.write("   - Graph_Summary.png: Statistical summary\n\n")
            
            f.write("2. CSV Data:\n")
            f.write("   - Detailed_Data.csv: Results per image\n")
            f.write("   - Summary_By_Day.csv: Statistics by day\n\n")
            
            f.write("3. Processed Images:\n")
            for day in sorted(self.data['days']):
                f.write(f"   - Day_{day}/: Images from day {day}\n")
            
            f.write("\n" + "="*60 + "\n")
            f.write(" END OF REPORT\n")
            f.write("="*60 + "\n")
        
        print(f"✅ Report created: {report_name}")
        return report_name
    
    # ============================================================================
    # MAIN FLOW
    # ============================================================================
    
    def execute(self):
        """Executes the complete step-by-step flow"""
        self.show_header()
        
        # STEP 1: Basic information
        self.step1_basic_information()
        
        # STEP 2: Process by days
        self.step2_process_by_days()
        
        if not self.data['days']:
            print("\n❌ No days registered. Analysis cancelled.")
            return
        
        # STEP 3: Process images
        base_folder = self.step3_process_images()
        
        # STEP 4: Statistical analysis
        results = self.step4_statistical_analysis()
        
        if results:
            # STEP 5: Graphs
            graph_files = self.step5_generate_graphs(results, base_folder)
            
            # STEP 6: CSV
            csv_files = self.step6_save_to_csv(results, base_folder)
            
            # STEP 7: Report
            report_file = self.step7_create_report(results, base_folder)
            
            # FINAL SUMMARY
            self.show_final_summary(results, base_folder)
    
    def show_final_summary(self, results, base_folder):
        """Shows final summary"""
        print("\n" + "="*60)
        print(" ✅ ANALYSIS COMPLETED")
        print("="*60)
        
        total_images = sum(len(imgs) for imgs in self.data['images_per_day'].values())
        
        print(f"\n📊 SUMMARY:")
        print(f"   Experiment: {self.data['experiment_name']}")
        print(f"   Days: {len(self.data['days'])}")
        print(f"   Total images: {total_images}")
        
        if results and len(results['days']) > 1:
            change = results['averages'][-1] - results['averages'][0]
            direction = "📈 INCREASE" if change > 0 else "📉 DECREASE"
            print(f"   Trend: {direction} of {abs(change):.1f}% in lipids")
        
        print(f"\n📁 RESULTS in '{base_folder}/':")
        print(f"   📈 3 graph files (PNG)")
        print(f"   📊 2 CSV files")
        print(f"   📝 1 text report")
        print(f"   🖼️  {total_images} processed images")
        
        print(f"\n📍 To view results:")
        print(f"   Open folder: {base_folder}")
        print("\n" + "="*60)


# ============================================================================
# EXECUTION
# ============================================================================

if __name__ == "__main__":
    system = CellCultureAnalysisSystem()
    system.execute()
