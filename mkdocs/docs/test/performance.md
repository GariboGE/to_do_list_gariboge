# JMETER CONFIGURATION FOR THE TEST

---

## **Configuration Summary**

This documentation describes the initial configuration used in your performance test with **Apache JMeter**, specifying the number of users, routes, and other key parameters.

---

## 🔹 **Main Parameters**

### **Number of Concurrent Users**  
- **Concurrent Users (Threads):** 5  
  - Configuration of **Thread Groups** with a total of **5 threads** to simulate concurrent users.

---

### **HTTP Request Details**

- **Server URL:**  
  - `https://to-do-list-gariboge.onrender.com`

- **Specific Route for Requests:**  
  - **Login:** `/auth/login`

---

### **Test Plan Configuration**

1. **Test Plan (`Test Plan.jmx`)**  
   - Configured to execute requests on the server `https://to-do-list-gariboge.onrender.com`.
   - Utilized **Thread Groups** to simulate concurrent users.

2. **Listeners (Result Elements)**  
- **View Results Tree**  
  - Configured to export responses as an image (`View Results Tree.png`).
  - Provides details such as response time, error messages, and other parameters.

- **Summary Report**  
  - Exports summarized metrics to a file `sumaryreport`.
  - Contains essential data such as response time, request success rates, and other relevant values.

---

### **Exported Files**

| File                    | Description                                                                                     |
|-------------------------|-------------------------------------------------------------------------------------------------|
| [`sumaryreport`](sumaryreport)        | CSV report containing summarized data (response times, success, and failures).                 |
| [`View Results Tree.png`](View\ Results\ Tree.png)  | Image exported from the **View Results Tree**, showing visual details of responses.             |
| [`Test Plan.jmx`](Test\ Plan.jmx)         | Complete configuration file for your test plan.                                                |

---
## **Conclusion**

The initial JMeter test configuration included:

- **5 concurrent users** simulated through **Thread Groups**.
- Tests directed to the endpoint `/auth/login` on the server `https://to-do-list-gariboge.onrender.com`.
- Data exported in both visual images and CSV reports.

This configuration allows for in-depth analysis of server behavior and performance, verifying critical metrics such as response times and success rates.

---
