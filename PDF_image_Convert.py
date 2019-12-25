import PySimpleGUI as sg
import os, fnmatch, xlsxwriter
from PyPDF3 import PdfFileReader, PdfFileWriter
import subprocess
from PIL import Image


#create the data coloumn set
layout = [
    [sg.Text('Script output....', size=(40, 1))],      
    [sg.Output(size=(88, 20), key='outfield')],   
    [sg.Text('Choose Interview Date'), sg.InputText(default_text ='',key='date', size=(20,1)), sg.CalendarButton(button_text='Date Picker', target='date', format='%m/%d/%y')],
    [sg.Text('PDF File to Convert'), sg.InputText(key='folder'), sg.FolderBrowse(button_text = 'Browse PDF', target='folder')],
    [sg.Button(button_text='Convert'), sg.Button(button_text='Close')]
]

#extract images from PDF file
def image_exporter(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cmd = ['pdfimages', '-j', pdf_path, 
           f'{output_dir}/{pdf_path}']
    subprocess.call(cmd)
    window['outfield'].update('\n'.join(os.listdir(output_dir)))

#create the excel extraction data from PDF function  
def pdf_data(pathname):
    school_name = []
    for pdf_page in os.listdir(pathname):
        if pdf_page.endswith("pdf"): 
            #open the pdf obj
            pdf_obj = open(f"{pathname}/{pdf_page}", 'rb')
            #read each pdf 
            pdf_read = PdfFileReader(pdf_obj)
            #get the page
            pdf_txt = pdf_read.getPage(0).extractText().split('\n')
            #get the name
            index_name = pdf_txt.index('AAMC ID: ')
            full_name = pdf_txt[index_name+1].split(', ')
            #get the school
            school = pdf_txt.index('Most Recent Medical School: ')
            #get AAMC ID 
            aamc_id = pdf_txt.index('Primary Care (Primary Care (Primary Care))')

            school_name.append([pdf_txt[aamc_id+1].split()[0], full_name[1] + full_name[0], pdf_txt[school+1]])

    #create the excel_sheet 
    workbook = xlsxwriter.Workbook('applicant_image_table.xlsx')
    worksheet = workbook.add_worksheet()
    cell_format = workbook.add_format()

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 40)
    #center page horizontal
    worksheet.center_horizontally()
    #show gridlines
    worksheet.hide_gridlines(0)
    #cell center
    cell_format.set_align('vcenter')
    #text wrap
    cell_format.set_text_wrap()
    #cell font size
    cell_format.set_font_size(12)
    #Header Center
    worksheet.set_header(f'&CSAMC FM Applicants {values["date"]}')
    # Default row size 
    worksheet.set_default_row(125)
    #insert images
    image_row = 0
    image_column = 0

    name_row = 0 
    name_column = 1

    #iterate through the school name array 
    for applicant in school_name: 
        #image insert
        worksheet.insert_image(image_row, image_column, f"{pathname}/thumbnails/{applicant[0]}.jpg", {'x_scale': 1, 'y_scale': 1, 'x_offset': 5, 'y_offset': 5, 'positioning': 1}) #position 1 allows change image size relative cell size
        image_row += 1

        #insert name_school
        worksheet.write(name_row, name_column, applicant[1] + "\n" + applicant[2], cell_format)
        name_row += 1
    
    print(f"Created: {workbook.filename}")

    workbook.close()


#create the window
window = sg.Window('PDF Image Extractor & Table Creator', default_element_size=(50, 2)).Layout(layout)

#read and loop window setup
while True: 
    event, values = window.read()
    
    #if close button chosen
    if event in (None, 'Close'):
        print ('Cancel selected')
        break

    try:
        current_dir = os.chdir(values['folder'])
        #list files in current
        listOfFiles = os.listdir('.')
        pattern = "*.pdf"
    
        #start loop each pdf files and create the images dir 
        for entry in listOfFiles:
            if fnmatch.fnmatch(entry, pattern):
                image_exporter(entry, output_dir='images')

        imagefolder = values['folder'] + '/images'
        os.makedirs(f"{values['folder']}/thumbnails")

        for images in os.listdir(imagefolder):
        #convert into defined thumbnail size  
            im = Image.open(imagefolder + "/" + images)
            width, height = im.size
            size = 150, 150

            if (width, height) >= size: 
                im.thumbnail(size)
                im.save(f"{values['folder']}/thumbnails/{images}_thumb.jpg")

        for small_thumb in os.listdir(f"{values['folder']}/thumbnails"):
            #remove any small size empty/blank files
            if os.path.getsize(f"{values['folder']}/thumbnails/{small_thumb}") < 1000:
                os.remove(f"{values['folder']}/thumbnails/{small_thumb}")
            
            #rename the files into their respective AAMC ID 
            elif small_thumb.endswith("jpg"):
                aamc_id = small_thumb.split('_')[1]
                print (f"Thubnail produced: {aamc_id}.jpg")
                os.rename(f"{values['folder']}/thumbnails/{small_thumb}", f"{values['folder']}/thumbnails/{aamc_id}.jpg")

        #execute the PDF extract function
        pdf_data(values['folder'])
        

                     
    except:
        sg.popup("Path Incomplete or None Found!")



window.close()
