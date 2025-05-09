from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
import time
import pandas as pd

class CleartripFlightSearch:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.results = []

    def handle_popups(self):
        try:
            pop_up = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='pb-1 px-1 flex flex-middle nmx-1']"))
            )
            pop_up.click()
            print("Popup handled")
        except TimeoutException:
            print("No popup appeared within 30 seconds, moving on...")

    def open_site(self):
        self.driver.get("https://www.cleartrip.com")
        time.sleep(5)

    def select_flights_tab(self):
        try:
            flights_tab = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "(//div[@class='sc-fYsHOw ibTNYZ lob-card-subtitle-container'])[1]"))
            )
            flights_tab.click()
        except:
            print("Flights tab not found or already on flights page.")

    def enter_from_city(self, source_city):
        try:
            from_city = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "(//input[@class='w-100p fs-16 fw-500 c-neutral-900'])[1]"))
            )
            from_city.clear()
            from_city.send_keys(source_city)
            required_city = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "(//div[@class='airport-code br-2 my-2 ml-3 mr-4 bg-neutral-300 c-neutral-700 flex fw-600 pt-1 pb-1 w-10'])[1]"))
            )
            required_city.click()
            time.sleep(3)
        except Exception as e:
            print(f"Error entering source city: {e}")

    def enter_to_city(self, destination_city):
        try:
            to_city = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Where to?']"))
            )
            to_city.clear()
            to_city.send_keys(destination_city)
            xpaths = [
                f"//p[@class='tt-ellipsis o-hidden fs-14 fw-500' and contains(text(), '{destination_city}')]",
                f"//div[contains(@class, 'airport-code') and contains(text(), '{destination_city}')]",
                f"//div[contains(@class, 'to-city') and contains(text(), '{destination_city}')]"
            ]
            for xpath in xpaths:
                try:
                    required_city = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    required_city.click()
                    print(f"Successfully selected destination: {destination_city}")
                    time.sleep(3)
                    return
                except:
                    continue
            first_suggestion = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//ul[@class='to-city-suggestions']/li[1]"))
            )
            first_suggestion.click()
            print(f"Selected first suggestion for destination: {destination_city}")
            time.sleep(3)
        except Exception as e:
            print(f"Error entering destination city {destination_city}: {e}")

    def select_departure_date(self):
        try:
            date_input = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='dateSelectOnward']"))
            )
            date_input.click()
            specific_date = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Thu May 15 2025']"))
            )
            specific_date.click()
            time.sleep(2)
        except Exception as e:
            print(f"Unable to select departure date: {e}")

    def select_return_date(self):
        try:
            date_input = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='dateSelectReturn']"))
            )
            date_input.click()
            specific_date = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Fri May 16 2025']"))
            )
            specific_date.click()
            time.sleep(2)
        except Exception as e:
            print(f"Unable to select return date: {e}")

    def search_flights(self):
        try:
            search_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='sc-dAlyuH hzVhEm flex-1']"))
            )
            search_button.click()
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '₹')]"))
            )
            print("Search results loaded successfully")
        except Exception as e:
            print(f"Error during search: {e}")

    # def find_price(self, destination):
    #     try:
    #         n=1
    #         prices = []
    #         for n in range(1, 6):  # Top 5 prices
    #             xpath = f"(//p[contains(@class, 'm-0 fs-6 fw-700 c-neutral-900 ta-right')])[{n}]"
    #             print(xpath)
    #             try:
    #                 elem = self.driver.find_element(By.XPATH, xpath)
    #                 price_text = elem.text.replace("₹", "").replace(",", "").strip()
    #                 if price_text.isdigit():
    #                     prices.append(int(price_text))
    #             except NoSuchElementException:
    #                 print(f"⚠️ Price element not found at index {n}")
    #                 continue

    #         if prices:
    #             print(f"\n💰 Top 5 Cheapest Prices for {destination}: {prices}")
    #             self.results.append({
    #                 "From": "BLR",
    #                 "To": destination,
    #                 "Top 5 Prices": prices
    #                     })
    #         else:
    #             print(f"⚠️ No prices found for {destination}")
    #             self.results.append({
    #                 "From": "BLR",
    #                 "To": destination,
    #                 "Top 5 Prices": "No prices found"
    #             })

    #     except Exception as e:
    #         print(f"❌ Error finding prices for {destination}: {e}")
    #         self.results.append({
    #             "From": "BLR",
    #             "To": destination,
    #             "Top 5 Prices": f"Error: {str(e)}"
    #         })
    def find_price(self, destination):
        try:
            prices = []
            flights = []

            for n in range(1, 6):  # Top 5 results
                price_xpath = f"(//p[contains(@class, 'm-0 fs-6 fw-700 c-neutral-900 ta-right')])[{n}]"
                flight_xpath = f"(//p[contains(@class, 'to-ellipsis o-hidden ws-nowrap c-neutral-700 fs-1')])[{n}]"
                print(price_xpath)
                print(flight_xpath)

                try:
                    # Get price
                    price_elem = self.driver.find_element(By.XPATH, price_xpath)
                    price_text = price_elem.text.replace("₹", "").replace(",", "").strip()

                    # Get flight name
                    flight_elem = self.driver.find_element(By.XPATH, flight_xpath)
                    flight_text = flight_elem.text.strip()

                    if price_text.isdigit():
                        prices.append(int(price_text))
                        flights.append(flight_text)

                except NoSuchElementException:
                    print(f"⚠️ Missing element at index {n}")
                    continue

            if prices and flights:
                print(f"\nFrom: BLR\nTo: {destination}")
                print(f"Flights: {', '.join(flights)}")
                print(f"Prices: {prices}")

                self.results.append({
                    "From": "BLR",
                    "To": destination,
                    "Flights": flights,
                    "Top 5 Prices": prices
                })
            else:
                print(f"\nFrom: BLR\nTo: {destination}")
                print("Flights: No flights found")
                print("Prices: No prices found")
                self.results.append({
                    "From": "BLR",
                    "To": destination,
                    "Flights": "No flights found",
                    "Top 5 Prices": "No prices found"
                })

        except Exception as e:
            print(f"\n❌ Error fetching data for {destination}: {e}")
            self.results.append({
                "From": "BLR",
                "To": destination,
                "Flights": "Error",
                "Top 5 Prices": f"Error: {str(e)}"
        })

    def save_results(self):
        df = pd.DataFrame(self.results)
        df.to_csv("flight_prices.csv", index=False)
        print("Results saved to flight_prices.csv")

    def close(self):
        self.driver.quit()

    def run_for_destinations(self, from_city, destinations):
        self.open_site()
        self.handle_popups()
        self.select_flights_tab()
        self.handle_popups()

        for destination in destinations:
            try:
                print(f"\n--- Searching flights from {from_city} to {destination} ---")
                self.enter_from_city(from_city)
                self.enter_to_city(destination)
                self.select_departure_date()
                self.select_return_date()
                self.search_flights()
                self.find_price(destination)
                self.driver.back()
                time.sleep(5)
            except Exception as e:
                print(f"Error processing destination {destination}: {e}")

        self.save_results()
        self.close()


if __name__ == "__main__":
    source_city = "BLR"
    destination_cities = ["DEL", "CCU", "Chennai", "HYD"]
    flight_search = CleartripFlightSearch()
    flight_search.run_for_destinations(source_city, destination_cities)
