from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import datetime
import os

# Initialize the driver
driver = None

# URL aplikasi web Anda yang berjalan secara lokal
base_url = "http://localhost:3000"

# Ukuran layar untuk diuji
screen_widths = [320]

# Test log list
test_logs = []

# Initialize log file
log_file_path = "selenium_test_results.txt"

def log_message(message, test_type="INFO"):
    """Log message dengan timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{test_type}] {message}"
    test_logs.append(log_entry)
    print(log_entry)

def write_logs_to_file():
    """Tulis semua log ke file txt."""
    try:
        with open(log_file_path, 'w', encoding='utf-8') as f:
            f.write("=== SELENIUM TEST RESULTS ===\n")
            f.write(f"Test executed on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Base URL: {base_url}\n")
            f.write("="*50 + "\n\n")
            
            for log in test_logs:
                f.write(log + "\n")
        
        log_message(f"Test results saved to: {log_file_path}", "SUCCESS")
    except Exception as e:
        log_message(f"Failed to write logs to file: {e}", "ERROR")

def setup_driver(width):
    """Mengatur ukuran jendela browser."""
    global driver
    if driver is None:
        driver = webdriver.Chrome()
    
    driver.set_window_size(width, 800)
    driver.get(base_url)
    log_message(f"Testing pada resolusi: {width}px")
    time.sleep(3)  # Beri waktu halaman untuk memuat

def check_element_visibility(locator, description, timeout=10):
    """Mengecek apakah elemen terlihat dan mencatat jika tidak."""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        log_message(f"[OK] Elemen '{description}' terlihat.", "PASS")
        return element
    except TimeoutException:
        log_message(f"[GAGAL] Elemen '{description}' tidak terlihat dalam {timeout} detik.", "FAIL")
        return None
    except Exception as e:
        log_message(f"[GAGAL] Elemen '{description}' tidak ditemukan. Error: {e}", "FAIL")
        return None

def check_element_exists(locator, description):
    """Mengecek apakah elemen ada di DOM (tidak harus terlihat)."""
    try:
        element = driver.find_element(*locator)
        log_message(f"[OK] Elemen '{description}' ada di DOM.", "PASS")
        return element
    except NoSuchElementException:
        log_message(f"[GAGAL] Elemen '{description}' tidak ada di DOM.", "FAIL")
        return None

def check_multiple_elements(locator, description):
    """Mengecek apakah ada beberapa elemen dengan selector yang sama."""
    try:
        elements = driver.find_elements(*locator)
        if elements:
            log_message(f"[OK] Ditemukan {len(elements)} elemen '{description}'.", "PASS")
            return elements
        else:
            log_message(f"[GAGAL] Tidak ada elemen '{description}' ditemukan.", "FAIL")
            return []
    except Exception as e:
        log_message(f"[GAGAL] Error saat mencari elemen '{description}': {e}", "FAIL")
        return []

def check_navigation(link_element, expected_url_part, link_text):
    """Mengecek link navigasi."""
    if link_element:
        log_message(f"Menguji link: {link_text}")
        try:
            original_url = driver.current_url
            link_element.click()
            time.sleep(3)  # Tunggu navigasi
            
            current_url = driver.current_url
            if expected_url_part in current_url:
                log_message(f"[OK] Navigasi ke '{current_url}' berhasil.", "PASS")
                return True
            else:
                log_message(f"[GAGAL] Navigasi untuk '{link_text}'. URL saat ini: '{current_url}', diharapkan mengandung: '{expected_url_part}'.", "FAIL")
                return False
        except Exception as e:
            log_message(f"[GAGAL] Error saat mengklik link '{link_text}': {e}", "FAIL")
            return False
    else:
        log_message(f"[GAGAL] Link element '{link_text}' tidak tersedia untuk diklik.", "FAIL")
        return False

def navigate_to_page(url_path, page_name):
    """Navigasi langsung ke halaman tertentu."""
    try:
        full_url = f"{base_url}{url_path}"
        driver.get(full_url)
        time.sleep(3)
        log_message(f"Navigasi ke halaman '{page_name}' ({full_url})", "INFO")
        return True
    except Exception as e:
        log_message(f"Gagal navigasi ke '{page_name}': {e}", "FAIL")
        return False

def capture_issues(width, section, issue_description):
    """Mencatat isu yang ditemukan."""
    issue_msg = f"!! ISU DITEMUKAN ({width}px) !! - Bagian: {section} - Deskripsi: {issue_description}"
    log_message(issue_msg, "ISSUE")
    
    # Optional: Save screenshot
    try:
        screenshot_name = f"issue_{width}px_{section.replace(' ', '_')}_{int(time.time())}.png"
        driver.save_screenshot(screenshot_name)
        log_message(f"Screenshot disimpan: {screenshot_name}", "INFO")
    except Exception as e:
        log_message(f"Gagal menyimpan screenshot: {e}", "ERROR")

def test_home_page_components(width):
    """Test semua komponen UI di halaman Home."""
    log_message(f"\n=== TESTING HOME PAGE COMPONENTS ({width}px) ===", "INFO")
    
    # Navigate to home page
    navigate_to_page("/", "Home")
    
    # Test page title
    try:
        page_title = driver.title
        if "MicroClimate" in page_title:  # Adjust based on actual title
            log_message(f"[OK] Judul halaman: '{page_title}'", "PASS")
        else:
            capture_issues(width, "Home Page", f"Judul halaman kosong atau tidak sesuai: '{page_title}'")
    except Exception as e:
        capture_issues(width, "Home Page", f"Error mendapatkan judul halaman: {e}")
    
    # Test Navbar component
    navbar = check_element_visibility((By.TAG_NAME, "nav"), "Navbar")
    if navbar:
        # Test logo
        logo = check_element_exists((By.CSS_SELECTOR, "img[alt='Logo'], .navbar-brand img"), "Logo")
        
        # Test navigation links
        nav_links = check_multiple_elements((By.CSS_SELECTOR, ".nav-link, .navbar-nav a"), "Navigation Links")
        
        # Test specific nav links
        home_link = check_element_exists((By.LINK_TEXT, "Home"), "Home Link")
        
    # Test Hero section
    hero_section = check_element_visibility((By.CSS_SELECTOR, ".hero, #hero, [class*='hero']"), "Hero Section")
    
    # Test Category section
    category_section = check_element_visibility((By.CSS_SELECTOR, ".category, #category, [class*='category']"), "Category Section")
    
    # Test Core Features section
    core_features = check_element_visibility((By.CSS_SELECTOR, ".core-fitur, #core-fitur, [class*='core'], [class*='fitur']"), "Core Features Section")
    
    # Test Card Features section
    card_features = check_multiple_elements((By.CSS_SELECTOR, ".card, [class*='card']"), "Card Features")
    
    # Test Alat section
    alat_section = check_element_visibility((By.CSS_SELECTOR, ".alat, #alat, [class*='alat']"), "Alat Section")
    
    # Test Launch section
    launch_section = check_element_visibility((By.CSS_SELECTOR, ".launch, #launch, [class*='launch']"), "Launch Section")
    
    # Test FAQ section
    faq_section = check_element_visibility((By.CSS_SELECTOR, ".faq, #faq, [class*='faq']"), "FAQ Section")
    
    # Test Footer
    footer = check_element_visibility((By.TAG_NAME, "footer"), "Footer")
    
    # Test Scroll to Top Button
    scroll_button = check_element_exists((By.CSS_SELECTOR, 'button[aria-label="Scroll to top"]'), "Scroll to Top Button")

def test_dashboard_page_components(width):
    """Test semua komponen UI di halaman Dashboard."""
    log_message(f"\n=== TESTING DASHBOARD PAGE COMPONENTS ({width}px) ===", "INFO")
    
    # Navigate to dashboard page
    if not navigate_to_page("/dashboard", "Dashboard"):
        return
    
    # Test sidebar
    sidebar = check_element_visibility((By.CSS_SELECTOR, ".sidebar, [class*='sidebar']"), "Sidebar")
    
    # Test sidebar toggle button
    toggle_button = check_element_visibility((By.CSS_SELECTOR, "svg, [class*='bars'], .fa-bars"), "Sidebar Toggle Button")
    
    # Test main content area
    main_content = check_element_visibility((By.CSS_SELECTOR, ".main, [style*='margin'], [style*='width']"), "Main Content Area")
    
    # Test dashboard sections and charts
    dashboard_sections = check_multiple_elements((By.CSS_SELECTOR, ".chart, [class*='chart'], .dashboard-sect, [class*='dashboard']"), "Dashboard Sections/Charts")
    
    # Test station navigation if present
    station_links = check_multiple_elements((By.CSS_SELECTOR, "a[href*='station'], [class*='station']"), "Station Links")
    
    # Test download section
    download_section = check_element_exists((By.CSS_SELECTOR, "a[href*='download'], [class*='download']"), "Download Section")

def test_kalimantan_page_components(width):
    """Test semua komponen UI di halaman Kalimantan."""
    log_message(f"\n=== TESTING KALIMANTAN PAGE COMPONENTS ({width}px) ===", "INFO")
    
    # Navigate to kalimantan page
    if not navigate_to_page("/kalimantan", "Kalimantan"):
        return
    
    # Test sidebar
    sidebar = check_element_visibility((By.CSS_SELECTOR, ".sidebar, [class*='sidebar']"), "Kalimantan Sidebar")
    
    # Test sidebar toggle button
    toggle_button = check_element_visibility((By.CSS_SELECTOR, "svg, [class*='bars'], .fa-bars"), "Kalimantan Sidebar Toggle")
    
    # Test main content area
    main_content = check_element_visibility((By.CSS_SELECTOR, ".main, [style*='margin'], [style*='width']"), "Kalimantan Main Content")
    
    # Test dashboard sections and charts
    dashboard_sections = check_multiple_elements((By.CSS_SELECTOR, ".chart, [class*='chart'], .dashboard-sect, [class*='dashboard']"), "Kalimantan Dashboard Sections")
    
    # Test station navigation
    station_links = check_multiple_elements((By.CSS_SELECTOR, "a[href*='station'], [class*='station']"), "Kalimantan Station Links")
    
    # Test download section
    download_section = check_element_exists((By.CSS_SELECTOR, "a[href*='download'], [class*='download']"), "Kalimantan Download Section")

def test_sebesi_page_components(width):
    """Test semua komponen UI di halaman Sebesi."""
    log_message(f"\n=== TESTING SEBESI PAGE COMPONENTS ({width}px) ===", "INFO")
    
    # Navigate to sebesi page
    if not navigate_to_page("/sebesi", "Sebesi"):
        return
    
    # Test sidebar
    sidebar = check_element_visibility((By.CSS_SELECTOR, ".sidebar, [class*='sidebar']"), "Sebesi Sidebar")
    
    # Test sidebar toggle button
    toggle_button = check_element_visibility((By.CSS_SELECTOR, "svg, [class*='bars'], .fa-bars"), "Sebesi Sidebar Toggle")
    
    # Test main content area
    main_content = check_element_visibility((By.CSS_SELECTOR, ".main, [style*='margin'], [style*='width']"), "Sebesi Main Content")
    
    # Test dashboard sections and charts
    dashboard_sections = check_multiple_elements((By.CSS_SELECTOR, ".chart, [class*='chart'], .dashboard-sect, [class*='dashboard']"), "Sebesi Dashboard Sections")
    
    # Test station navigation
    station_links = check_multiple_elements((By.CSS_SELECTOR, "a[href*='station'], [class*='station']"), "Sebesi Station Links")
    
    # Test download section
    download_section = check_element_exists((By.CSS_SELECTOR, "a[href*='download'], [class*='download']"), "Sebesi Download Section")

def test_navigation_links(width):
    """Test semua link navigasi utama."""
    log_message(f"\n=== TESTING MAIN NAVIGATION ({width}px) ===", "INFO")
    
    # Start from home page
    navigate_to_page("/", "Home")
    
    # Test main navigation links
    navigation_tests = [
        ("/", "Home", ""),
        ("/dashboard", "Dashboard", "dashboard"),
        ("/kalimantan", "Kalimantan", "kalimantan"), 
        ("/sebesi", "Sebesi", "sebesi")
    ]
    
    for url_path, page_name, expected_url_part in navigation_tests:
        log_message(f"Testing navigation to {page_name}")
        if navigate_to_page(url_path, page_name):
            current_url = driver.current_url
            if expected_url_part in current_url.lower():
                log_message(f"[OK] Successfully navigated to {page_name}", "PASS")
            else:
                log_message(f"[FAIL] Navigation to {page_name} failed. Current URL: {current_url}", "FAIL")
        time.sleep(2)

def test_dashboard_navigation(width):
    """Test navigasi dalam dashboard (station1, station2, download)."""
    log_message(f"\n=== TESTING DASHBOARD INTERNAL NAVIGATION ({width}px) ===", "INFO")
    
    # Navigate to dashboard first
    if not navigate_to_page("/dashboard", "Dashboard"):
        return
    
    # Test dashboard sub-routes
    dashboard_routes = [
        ("/dashboard/station1", "Dashboard Station 1"),
        ("/dashboard/station2", "Dashboard Station 2"),
        ("/dashboard/download", "Dashboard Download")
    ]
    
    for route, name in dashboard_routes:
        log_message(f"Testing {name}")
        if navigate_to_page(route, name):
            # Check if page loaded correctly
            time.sleep(2)
            page_content = check_element_exists((By.TAG_NAME, "body"), f"{name} Content")
            if page_content:
                log_message(f"[OK] {name} loaded successfully", "PASS")
            else:
                log_message(f"[FAIL] {name} failed to load properly", "FAIL")

def test_kalimantan_navigation(width):
    """Test navigasi dalam kalimantan (station1, station2, download)."""
    log_message(f"\n=== TESTING KALIMANTAN INTERNAL NAVIGATION ({width}px) ===", "INFO")
    
    # Navigate to kalimantan first
    if not navigate_to_page("/kalimantan", "Kalimantan"):
        return
    
    # Test kalimantan sub-routes
    kalimantan_routes = [
        ("/kalimantan/station1", "Kalimantan Station 1"),
        ("/kalimantan/station2", "Kalimantan Station 2"),
        ("/kalimantan/download", "Kalimantan Download")
    ]
    
    for route, name in kalimantan_routes:
        log_message(f"Testing {name}")
        if navigate_to_page(route, name):
            # Check if page loaded correctly
            time.sleep(2)
            page_content = check_element_exists((By.TAG_NAME, "body"), f"{name} Content")
            if page_content:
                log_message(f"[OK] {name} loaded successfully", "PASS")
            else:
                log_message(f"[FAIL] {name} failed to load properly", "FAIL")

def test_sebesi_navigation(width):
    """Test navigasi dalam sebesi (station1, station2, download)."""
    log_message(f"\n=== TESTING SEBESI INTERNAL NAVIGATION ({width}px) ===", "INFO")
    
    # Navigate to sebesi first
    if not navigate_to_page("/sebesi", "Sebesi"):
        return
    
    # Test sebesi sub-routes
    sebesi_routes = [
        ("/sebesi/station1", "Sebesi Station 1"),
        ("/sebesi/station2", "Sebesi Station 2"),
        ("/sebesi/download", "Sebesi Download")
    ]
    
    for route, name in sebesi_routes:
        log_message(f"Testing {name}")
        if navigate_to_page(route, name):
            # Check if page loaded correctly
            time.sleep(2)
            page_content = check_element_exists((By.TAG_NAME, "body"), f"{name} Content")
            if page_content:
                log_message(f"[OK] {name} loaded successfully", "PASS")
            else:
                log_message(f"[FAIL] {name} failed to load properly", "FAIL")

def test_responsive_layout(width):
    """Test responsivitas layout pada resolusi tertentu."""
    log_message(f"\n=== TESTING RESPONSIVE LAYOUT ({width}px) ===", "INFO")
    
    # Navigate to home page for responsive testing
    navigate_to_page("/", "Home")
    
    # Check for horizontal scrollbar (indicates layout issues)
    try:
        scroll_width = driver.execute_script("return document.body.scrollWidth")
        window_width = driver.execute_script("return window.innerWidth")
        
        if scroll_width > window_width + 5:  # Allow 5px tolerance
            capture_issues(width, "Responsive Layout", 
                         f"Horizontal scrollbar detected. Body width: {scroll_width}px, Window width: {window_width}px")
        else:
            log_message(f"[OK] No horizontal scrollbar. Layout fits in {width}px", "PASS")
    except Exception as e:
        log_message(f"[ERROR] Failed to check scrollbar: {e}", "ERROR")
    
    # Test navbar responsiveness
    if width <= 768:  # Mobile/tablet view
        navbar_toggle = check_element_exists((By.CSS_SELECTOR, ".navbar-toggle, .navbar-toggler, [data-bs-toggle='collapse']"), "Mobile Navbar Toggle")
        if navbar_toggle:
            log_message(f"[OK] Mobile navbar toggle found at {width}px", "PASS")
        else:
            capture_issues(width, "Responsive Navbar", "Mobile navbar toggle not found")
    
    # Test sidebar responsiveness for dashboard pages
    for page_path in ["/dashboard", "/kalimantan", "/sebesi"]:
        navigate_to_page(page_path, f"Responsive {page_path}")
        
        # Check if sidebar adapts to screen size
        sidebar = check_element_exists((By.CSS_SELECTOR, ".sidebar, [class*='sidebar']"), f"Sidebar in {page_path}")
        if sidebar:
            try:
                sidebar_width = driver.execute_script("return arguments[0].offsetWidth", sidebar)
                if width <= 768 and sidebar_width > width * 0.8:
                    capture_issues(width, f"Responsive Sidebar {page_path}", 
                                 f"Sidebar too wide for mobile: {sidebar_width}px on {width}px screen")
                else:
                    log_message(f"[OK] Sidebar width appropriate: {sidebar_width}px on {width}px", "PASS")
            except Exception as e:
                log_message(f"[ERROR] Failed to check sidebar width: {e}", "ERROR")

# --- Mulai Testing ---
def main_test():
    """Fungsi utama untuk menjalankan semua test."""
    global driver
    
    try:
        log_message("=== MEMULAI SELENIUM TESTING ===", "INFO")
        log_message(f"Base URL: {base_url}", "INFO")
        log_message(f"Screen resolutions to test: {screen_widths}", "INFO")
        
        # Initialize driver
        driver = webdriver.Chrome()
        log_message("Chrome WebDriver initialized successfully", "SUCCESS")
        
        # Test untuk setiap resolusi
        for width in screen_widths:
            log_message(f"\n{'='*60}", "INFO")
            log_message(f"TESTING RESOLUSI: {width}px", "INFO")
            log_message(f"{'='*60}", "INFO")
            
            # Setup driver untuk resolusi ini
            setup_driver(width)
            
            # Test UI Components untuk semua halaman
            test_home_page_components(width)
            test_dashboard_page_components(width)
            test_kalimantan_page_components(width)
            test_sebesi_page_components(width)
            
            # Test Navigation
            test_navigation_links(width)
            test_dashboard_navigation(width)
            test_kalimantan_navigation(width)
            test_sebesi_navigation(width)
            
            # Test Responsiveness
            test_responsive_layout(width)
            
            log_message(f"--- SELESAI TESTING RESOLUSI {width}px ---\n", "INFO")
        
        log_message("=== SEMUA TESTING SELESAI ===", "SUCCESS")
        
    except Exception as e:
        log_message(f"CRITICAL ERROR: {e}", "ERROR")
        
    finally:
        # Tutup browser
        if driver:
            log_message("Menutup browser...", "INFO")
            time.sleep(3)  # Beri waktu untuk melihat hasil
            driver.quit()
            log_message("Browser ditutup", "INFO")
        
        # Tulis log ke file
        write_logs_to_file()
        
        # Summary
        total_logs = len(test_logs)
        pass_count = len([log for log in test_logs if "[PASS]" in log])
        fail_count = len([log for log in test_logs if "[FAIL]" in log])
        issue_count = len([log for log in test_logs if "[ISSUE]" in log])
        
        print(f"\n{'='*50}")
        print("TEST SUMMARY:")
        print(f"Total log entries: {total_logs}")
        print(f"Passed tests: {pass_count}")
        print(f"Failed tests: {fail_count}")
        print(f"Issues found: {issue_count}")
        print(f"Test results saved to: {log_file_path}")
        print(f"{'='*50}")

if __name__ == "__main__":
    main_test()