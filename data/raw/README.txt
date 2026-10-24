
This document provides detailed column descriptions for the datasets used in the project. Each section corresponds to a specific file containing structured data.

---

1. Support_Points.csv:
- points_specified: The exact coordinates of a navigation point in the format (x, y, z). Data type: string (tuple representation). Unit: meters.
- labels: Assigned labels for each navigation point, typically used for identification or categorization. Data type: string. Unit: not applicable.

---

2. Class_Based_Storage.csv:
- Location: The initial storage location of products within the warehouse. Data type: string. Unit: not applicable.
- ABCCOD: A classification code categorizing the product. Data type: string. Unit: not applicable.
- col_1 to col_18: Encoded details of products stored at the location, formatted as 'product_code;quantity'. Data type: string. Unit: quantity in units.

---

3. Customer_Order.csv:
- codCustomer: A unique identifier for each customer. Data type: string. Unit: not applicable.
- orderNumber: The unique number assigned to a customer's order. Data type: integer. Unit: not applicable.
- orderToCollect: The sequence number of the order for collection. Data type: integer. Unit: not applicable.
- Reference: The reference code of the item included in the order. Data type: string. Unit: not applicable.
- Size (US): The size specification of the item in US sizing standards. Data type: float. Unit: not applicable.
- quantity (units): The total number of items in the order. Data type: integer. Unit: units.
- creationDate: The timestamp when the order was created. Data type: datetime. Unit: not applicable.
- waveNumber: The identifier for the picking wave associated with the order. Data type: integer. Unit: not applicable.
- operator: The individual responsible for handling the order. Data type: string. Unit: not applicable.

---

4. Dedicated_Storage.csv:
- Location: The initial storage location of products within the warehouse. Data type: string. Unit: not applicable.
- XYZCOD: A classification code categorizing the product. Data type: string. Unit: not applicable.
- col_1 to col_18: Encoded details of products stored at the location, formatted as 'product_code;quantity'. Data type: string. Unit: quantity in units.

---

5. Hybrid_Storage.csv:
- Location: The initial storage location of products within the warehouse. Data type: string. Unit: not applicable.
- XYZCOD: A classification code categorizing the product. Data type: string. Unit: not applicable.
- col_1 to col_18: Encoded details of products stored at the location, formatted as 'product_code;quantity'. Data type: string. Unit: quantity in units.

---

6. Picking_Wave.csv:
- waveNumber: The identifier for the picking wave. Data type: integer. Unit: not applicable.
- reference: The reference code for the item to be picked. Data type: string. Unit: not applicable.
- Size (US): The size of the item in US sizing standards. Data type: float. Unit: not applicable.
- quantityToPick (units): The total number of units to be picked during the wave. Data type: integer. Unit: units.
- locations: The storage location(s) of the items to be picked. Data type: string. Unit: not applicable.
- operator: The individual assigned to perform the picking tasks. Data type: string. Unit: not applicable.

---

7. Product.csv:
- Reference: A unique identifier for the product. Data type: string. Unit: not applicable.
- ABCCOD: A classification code categorizing the product. Data type: string. Unit: not applicable.
- Sector: The warehouse sector where the product is typically stored. Data type: string. Unit: not applicable.

---

8. Random_Storage.csv:
- originalLocation: The initial storage location of products within the warehouse. Data type: string. Unit: not applicable.
- col_1 to col_18: Encoded details of products stored at the location, formatted as 'product_code;quantity'. Data type: string. Unit: quantity in units.

---

9. Storage_Location.csv:
- originalLocation: The original storage location of the product in the warehouse. Data type: string. Unit: not applicable.
- position: The concatenated coordinates of the storage position in the warehouse. Data type: string. Unit: not applicable.
- x: The X-coordinate of the storage position in meters. Data type: integer. Unit: meters.
- y: The Y-coordinate of the storage position in meters. Data type: integer. Unit: meters.
- z: The Z-coordinate of the storage position in meters. Data type: integer. Unit: meters.

