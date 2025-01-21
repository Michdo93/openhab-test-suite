# **openhab-test-suite**  
A comprehensive testing library for validating and interacting with openHAB installations.  

**openhab-test-suite** simplifies the process of testing items, rules, and things in openHAB systems. The library provides an easy-to-use Python API that interacts with the openHAB REST API, enabling automated testing of various components in your smart home environment.  

---

## **Features**  
- **Item Testing**: Validate item states and ensure proper functionality for various types (e.g., Switch, String, Color).  
- **Thing Testing**: Verify thing statuses (e.g., ONLINE, OFFLINE, PENDING) and troubleshoot connectivity issues.  
- **Rule Testing**: Manage and execute rules programmatically to ensure their expected behavior.  
- Supports local and cloud-based openHAB instances.  
- Designed for developers and testers working on openHAB integrations.  

---

## **Why use openhab-test-suite?**  
This library helps identify issues quickly, automate validation processes, and maintain a reliable smart home setup. Whether you are building new automations or troubleshooting an existing configuration, **openhab-test-suite** provides the tools you need.  

---

## **Requirements**  
- Python 3.7 or newer  
- `python-openhab-crud` library (install using `pip install python-openhab-crud`)
- `python-openhab-itemevents` library (install using `pip install python-openhab-itemevents`)  
- A running openHAB server with REST API enabled (you have to enable Basic Authentication)

---

## **Installation**

### **Install via pip**

To install the package using pip, simply run:

```bash
pip install openhab-test-suite
```

### **Manual Installation**

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-repo/openhab-test-suite.git
   cd openhab-test-suite
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your openHAB server settings in your Python code.  

---

## **Usage**  

Here is an example of how to use the library for basic operations:  

### Initialize the Connector  
```python
from openhab_test_suite import OpenHABConnector

connector = OpenHABConnector(
    url="http://openhab-server:8080",
    username="your-username",
    password="your-password"
)
```

### Test Items  
```python
from openhab_test_suite import ItemTester

itemTester = ItemTester(connector)

# Check if an item is ONLINE
isOnline = itemTester.isItemOnline("LightSwitch1")
print(f"LightSwitch1 online status: {isOnline}")
```

### Test Rules  
```python
from openhab_test_suite import RuleTester

ruleTester = RuleTester(connector)

# Run a rule and verify the result
ruleTester.runRule("myRuleUID")
```

---

## **Full List of Methods**

### **OpenHABConnector**  
Handles communication with the openHAB REST API.

| Method         | Description                                                                                              |
|----------------|----------------------------------------------------------------------------------------------------------|
| `get(endpoint, header)` | Sends a GET request to the specified endpoint. Returns the response.                              |
| `post(endpoint, header, data)` | Sends a POST request to the specified endpoint with optional headers and data. Returns the response.  |
| `put(endpoint, header, data)` | Sends a PUT request to the specified endpoint with optional headers and data. Returns the response.   |

---

### **ItemTester**  
Provides methods to test and validate openHAB items.

| Method                     | Description                                                                                   |
|----------------------------|-----------------------------------------------------------------------------------------------|
| `isItemOnline(itemName)`   | Checks if the specified item is ONLINE.                                                       |
| `getItemState(itemName)`   | Retrieves the current state of an item.                                                       |
| `setItemState(itemName, value)` | Sets the state of an item to the specified value.                                               |
| `testItemState(itemName, expectedValue)` | Tests if the item's state matches the expected value.                                     |
| `sendCommand(itemName, command)` | Sends a command to the specified item.                                                           |

---

### **ThingTester**  
Provides methods to test and validate openHAB things.

| Method                     | Description                                                                                   |
|----------------------------|-----------------------------------------------------------------------------------------------|
| `isThingOnline(thingUID)`  | Checks if the specified thing is ONLINE.                                                      |
| `getThingStatus(thingUID)` | Retrieves the current status of a thing.                                                      |
| `testThingStatus(thingUID, expectedStatus)` | Tests if the thing's status matches the expected value.                                     |
| `enableThing(thingUID)`    | Enables the specified thing.                                                                  |
| `disableThing(thingUID)`   | Disables the specified thing.                                                                 |

---

### **RuleTester**  
Provides methods to manage and test openHAB rules.

| Method                     | Description                                                                                   |
|----------------------------|-----------------------------------------------------------------------------------------------|
| `runRule(ruleUid)`         | Executes a rule immediately.                                                                  |
| `enableRule(ruleUid)`      | Enables the specified rule.                                                                   |
| `disableRule(ruleUid)`     | Disables the specified rule.                                                                  |
| `testRuleExecution(ruleUid, expectedItem, expectedValue)` | Tests the execution of a rule and verifies the outcome by checking an item's state. |
| `isRuleActive(ruleUid)`    | Checks if the rule is active.                                                                 |
| `isRuleDisabled(ruleUid)`  | Checks if the rule is disabled.                                                               |
| `isRuleRunning(ruleUid)`   | Checks if the rule is currently running.                                                      |
| `isRuleIdle(ruleUid)`      | Checks if the rule is in the IDLE state.                                                      |
| `getRuleStatus(ruleUid)`   | Retrieves detailed status information about a rule.                                           |

---

## **Contributing**

We welcome contributions to improve **openhab-test-suite**!  

### How to contribute:  
1. Fork the repository.  
2. Create a new branch:  
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add your feature description"
   ```
4. Push to the branch:  
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.  

Please ensure your code adheres to PEP 8 guidelines and includes relevant documentation and tests.  

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  
