import time
import sys
from EraseSpaces import EraseSpaces
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bf
import csv
import re

class Main():
    def login(self):
        try:
            opti = Options()
            opti.set_headless(headless=True)
            br_path = str(sys.argv[1])
            browser = webdriver.Firefox(firefox_options=opti, executable_path=br_path)
            print('Headless Browser Invoked!')
            browser.implicitly_wait(10) #seconds
            browser.get('https://www.gruposdm.com/iniciar-sesion?back=my-account')
            print(browser.title)
            user_xpath = '/html/body/main/section/div/div/section/section/section/form/section/div[1]/div[1]/input'
            pass_xpath = '/html/body/main/section/div/div/section/section/section/form/section/div[2]/div[1]/div/input'
            browser.find_element_by_xpath(user_xpath).send_keys(sys.argv[2])
            browser.find_element_by_xpath(pass_xpath).send_keys(sys.argv[3])
            browser.find_element_by_xpath('//*[@id="submit-login"]').click()
            print('Loggin in')
            return browser
        except(KeyboardInterrupt):
            browser.close()
            print('Cerrando browser')
            raise

    def pag_principal(self, browser):
        index_list = []
        time.sleep(10)
        print('Getting index')
        browser.get('https://www.gruposdm.com/')
        page_soup = bf(browser.page_source, 'html.parser')
        ul_find = page_soup.find_all('ul')
        a_noclass = ul_find[1].find_all('a', {'class': None})
        for i in a_noclass:
            index_list.append({'link': i['href'], 'cat': i.contents[0]})
        print('All categories with link getted')
        #for i in index_list:
        #    print(i['link'])
        #    print(i['cat'])
        print(len(index_list))
        return index_list

    def c_index(self, browser, index_list):
        #FALTA HACER LAS LISTAS CON DICT, REGRESARA CATEGORIA Y LINK DEL PRODUCTO
        lista_links = []
        productos_list = []
        empty_list = []
        for i in index_list:
            j = 1
            while True:
                try:
                    time.sleep(10)
                    browser.get(str(i['link'])+'?page='+str(j))
                    print('Accediendo a '+i['cat']+' '+str(j))
                    page_soup = bf(browser.page_source, 'html.parser')
                    a_img = page_soup.find_all('a', {'class': 'thumbnail product-thumbnail'})
                    if(a_img == empty_list):
                        raise ValueError #Poner un ValueError instead
                    for k in a_img:
                        if(k['href'] not in lista_links):
                            productos_list.append({'cat': i['cat'], 'link': k['href']})
                            #print('\t'+k['href'])
                            lista_links.append(k['href'])
                    print('\tLinks obtenidos\n')
                    #print(productos_list)
                    j += 1
                    #for a in a_img:
                    #    print(a['href'])
                    #    print()
                except(KeyboardInterrupt):
                    print('Cerrando browser')
                    browser.close()
                    raise
                except(ValueError):
                    print('\tSiguiente index\n')
                    break
        print('Productos obtenidos')
        #print(productos_list)
        print(len(productos_list))
        return productos_list

    def c_prod(self, browser, productos_list):
        csv_list = []
        cont = 0
        num = 1
        for i in productos_list:
            time.sleep(10)
            print('Souping '+i['link'])
            browser.get(i['link'])
            page_soup = bf(browser.page_source, 'html.parser')
            price = page_soup.find('span', {'class': 'product-price', 'itemprop': 'price'})['content']
            ava = list(page_soup.find('span', {'id': 'product-availability'}).get_text())
            avail = EraseSpaces(ava)
            available = avail.list
            min = page_soup.find('div', {'class': 'input-group bootstrap-touchspin'}).find('input')['min']
            name = page_soup.find('h1', {'class': 'h1 page-title'}).find('span').contents[0]
            ref = page_soup.find('span', {'itemprop': 'sku'}).contents[0]
            desc = page_soup.find('div', {'class': 'rte-content'}).find_all('p')
            img = page_soup.find('img', {'class': 'img-fluid', 'itemprop': 'image'})['src']
            try:
                marca = page_soup.find('div', {'class': 'product_header_container clearfix'})
                marca = marca.find_all('span')[2].find('a').contents[0]
            except(AttributeError):
                print('\nProduct has no brand')
                marca = ''

            resi = self.def_residential(i['cat'])

            color = self.def_color(name)
            desc_all = ''
            for j in desc:
                desc_all = desc_all + j.get_text() + ' '

            try:
                ancho = re.search('Ancho: ([0-9A-Za-z]+)', desc_all).group(1)
            except:
                try:
                    ancho = re.search('Anchura: ([0-9A-Za-z]+)', desc_all).group(1)
                except:
                    try:
                        ancho = re.search('Ancho:(.....)', desc_all).group(1)
                    except:
                        try:
                            ancho = re.search('Anchura:(.....)', desc_all).group(1)
                        except:
                            print('\nAnchura not found')
                            ancho = ''

            try:
                fondo = re.search('Fondo: ([0-9A-Za-z]+)', desc_all).group(1)
            except:
                try:
                    fondo = re.search('Fondo:(.....)', desc_all).group(1)
                except:
                    print('\nFondo not found')
                    fondo = ''

            try:
                altura = re.search('Altura: ([0-9A-Za-z]+)', desc_all).group(1)
            except:
                try:
                    altura = re.search('Alto: ([0-9A-Za-z]+)', desc_all).group(1)
                except:
                    try:
                        altura = re.search('Altura:(.....)', desc_all).group(1)
                    except:
                        try:
                            altura = re.search('Alto:(.....)', desc_all).group(1)
                        except:
                            print('\nAltura not found')
                            altura = ''

            try:
                img2 = page_soup.find('div', {'class': 'js-qv-mask mask'}).find_all('img')
                img2_src = []
                for k in img2:
                    img2_src.append(k['src'])
                #print('\nDemas imagenes:')
                #print(img2_src)
                img_all = img + '|' + '|'.join(img2_src)
            except:
                print('Just 1 photo')
                img_all = img
            dict_pr = {
                'SKU': ref,
                'Parent SKU': '',
                'UPC': '',
                'tax:product_type': 'simple',
                'post_status': 'publish',
                'Product Title': name,
                'Short Description': desc_all,
                'Description': '',
                'tax:product_cat': i['cat'],
                'availability': available,
                'moq': min,
                'MAP': price,
                'regular_price': '',
                'attribute:pa_outdoor-use': '',
                'attribute:pa_color': color,
                'attribute_data:pa_color': '',
                'attribute_default:pa_color': '',
                'meta:attribute_pa_color': '',
                'attribute:pa_application': resi,
                'attribute:pa_arms': '',
                'attribute:pa_base-legs': '',
                'attribute:pa_structure-material': '',
                'attribute:pa_upholstery-material': '',
                'Product Width': ancho,
                'Product Depth': fondo,
                'Product Height': altura,
                'Product Weight': '',
                'attribute:pa_assembly': 'Si',
                'attribute:pa_warranty': '2 years',
                'attribute:pa_country-of-origin': 'China',
                'attribute:pa_style': '',
                'attribute:pa_care-instructions': '',
                'attribute:pa_weight-capacity': '',
                'tax:pwb-brand': marca,
                'Images': img_all
                }
            csv_list.append(dict_pr)
            cont += 1
            if(cont >= 200):
                self.do_csv(csv_list, num)
                cont = 0
               	num += 1
                csv_list = []
        return csv_list

    def def_color(self, name):
        if(re.findall('blanco', name) != []):
            color = 'blanco'
        elif(re.findall('negr', name) != []):
            color = 'negro'
        elif(re.findall('gris', name) != []):
            color = 'gris'
        elif(re.findall('turquesa', name) != []):
            color = 'turquesa'
        elif(re.findall('rosa', name) != []):
            color = 'rosa'
        elif(re.findall('azul', name) != []):
            color = 'azul'
        elif(re.findall('roj', name) != []):
            color = 'rojo'
        elif(re.findall('amarill', name) != []):
            color = 'amarillo'
        elif(re.findall('verde', name) != []):
            color = 'verde'
        elif(re.findall('transparente', name) != []):
            color = 'transparente'
        elif(re.findall('café', name) != []):
            color = 'café'
        elif(re.findall('cristal', name) != []):
            color = 'cristal'
        elif(re.findall('naranja', name) != []):
            color = 'naranja'
        else:
            color = ''
        return color

    def def_residential(self, cat):
        if(re.findall('HOSTELERÍA', cat) != []):
            return 'Comercial'
        elif(re.findall('OFICINA', cat) != []):
            return 'Comercial'
        else:
            return ''

    def do_csv(self, csv_list, num):
        keys = csv_list[0].keys()
        print('Creando documento')
        with open('productos '+str(num)+'.csv', 'w') as file:
            dict_writer = csv.DictWriter(file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(csv_list)
        print('Documento creado')

if(__name__=='__main__'):
    try:
        main = Main()
        browser = main.login()
        index_list = main.pag_principal(browser)
        productos_list = main.c_index(browser, index_list)
        csv_list = main.c_prod(browser, productos_list)
        try:
            main.do_csv(csv_list, 'final')
        except(IndexError):
            print('Lista sin elementos')
    except KeyboardInterrupt:
        print('Presione enter para finalizar')
        input()
    except Exception as e:
        print('ERROR')
        print(e)
    finally:
        try:
            print('Cerrando browser')
            browser.close()
            print('Presione enter para finalizar')
            input()
        except(NameError):
            print('Presione enter para finalizar')
            input()
