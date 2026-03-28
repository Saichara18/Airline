# Admin Flight Management - Quick Reference Guide

## Access Flight Management

1. **Login as Admin**
   - Email: `balugusaicharan@gmail.com`
   - Password: `Saicharan@2005`

2. **Navigate to Flights Panel**
   - Click "Admin Panel" from user dashboard
   - Click "View Flights" button OR "✈️ All Flights" under Manage

---

## ✅ How to Add a Flight

### Step-by-Step Guide

1. **Click "➕ Add Flight" button** (top right of flights page)

2. **Fill in the Flight Form:**
   - **Flight Number**: Unique identifier (e.g., AI-104, BA-505)
   - **Source**: Departure city (e.g., Delhi, Mumbai)
   - **Destination**: Arrival city (e.g., Bangalore, Goa)
   - **Departure Time**: HH:MM format (e.g., 08:00, 14:30)
   - **Arrival Time**: HH:MM format (e.g., 10:30, 17:00)
   - **Available Seats**: Number of seats (e.g., 150, 200)
   - **Price**: Per-ticket price in ₹ (e.g., 5999.00)

3. **Click "✅ Add Flight"** button

4. **Success Message**: "✅ Flight [NUMBER] added successfully!"

5. **Complete**: Flight appears in the flights list immediately

### Example Flight Entry
```
Flight Number:  SG-207
Source:         Singapore
Destination:    Kolkata
Departure:      22:30
Arrival:        04:45
Seats:          180
Price:          ₹7,499.00
```

---

## ❌ How to Delete a Flight

### Step-by-Step Guide

1. **Find the flight** you want to delete in the flights list

2. **Click "🗑️ Delete"** button in the Actions column

3. **Confirmation Dialog**: "Are you sure you want to delete this flight? All associated bookings will also be deleted."

4. **Confirm by clicking "OK"** (cannot undo this action!)

5. **Success Message**: "✅ Flight [NUMBER] deleted successfully!"

6. **Complete**: Flight removed from list and all bookings canceled

### ⚠️ Important Notes
- **IRREVERSIBLE**: Once deleted, the flight cannot be recovered
- **Cascading Delete**: All bookings for this flight will be canceled
- **Customers Notified**: (optional - implement customer notification feature)

---

## 📊 Flight Management Dashboard

### Flights Table Columns

| Column | Description |
|--------|-------------|
| **Flight Number** | Unique flight identifier (AI-101, BA-202, etc.) |
| **Route** | Shows "SOURCE → DESTINATION" |
| **Departure** | Departure time in HH:MM format |
| **Arrival** | Arrival time in HH:MM format |
| **Occupancy** | Visual progress bar showing seats booked/total |
| **Available Seats** | Number of seats still available |
| **Price** | Per-ticket price in Indian Rupees |
| **Actions** | 🗑️ Delete button for the flight |

### Example Screen View
```
✈️ All Flights

Total Flights: 10

Flight # | Route              | Departure | Arrival | Occupancy    | Seats | Price      | Actions
---------|------------------|-----------|---------|--------------|-------|------------|--------
AI-101   | Delhi → Mumbai    | 08:00     | 10:30   | ████░ 45%    | 55    | ₹5,999    | 🗑️ Delete
AI-102   | Delhi → Bangalore | 14:30     | 17:00   | ██████░ 65%  | 35    | ₹4,499    | 🗑️ Delete
BA-202   | London → Paris    | 10:30     | 12:30   | ██░ 20%      | 120   | ₹999      | 🗑️ Delete
```

---

## 🎨 Button Reference

### Add Flight Button
- **Location**: Top-right of flights page
- **Color**: Green (#4caf50)
- **Icon**: ➕
- **Action**: Opens add flight form
- **Access**: Admin only

### Delete Button  
- **Location**: End of each flight row (Actions column)
- **Color**: Red (#f44336)
- **Icon**: 🗑️
- **Action**: Shows confirmation, then deletes flight
- **Access**: Admin only

### Back Button
- **Location**: Top-right next to Add Flights
- **Color**: White with transparent background
- **Action**: Returns to Admin Dashboard
- **Access**: Admin only

---

## 📋 Flight Data Entry Guide

### Flight Number Format
- Typically Airline Code + Number
- Examples: AI-101, BA-202, UK-404, EK-505
- Must be UNIQUE (cannot duplicate)

### City Names
- Use full city names or standard abbreviations
- Examples: "Delhi", "Mumbai", "Bangalore", "London", "Paris"

### Time Format
- Use 24-hour format
- Format: HH:MM (hours:minutes)
- Valid: 08:00, 14:30, 22:15, 00:30
- Invalid: 8:00 (missing leading zero), 25:00 (invalid hour)

### Seat Capacity
- Enter total available seats
- Typical ranges: 50-250 seats
- Examples: 100, 150, 200

### Price Format
- Enter in Indian Rupees (₹)
- Decimal format allowed (e.g., 5999.00)
- Examples: 999, 4999.50, 9999.99

---

## ✨ Tips & Best Practices

### ✅ DO THIS
- ✅ Use consistent flight numbering system
- ✅ Enter realistic departure/arrival times
- ✅ Set seat capacity based on aircraft type
- ✅ Price competitively based on route
- ✅ Add flights well in advance
- ✅ Review occupancy regularly
- ✅ Delete flights that are no longer operating

### ❌ DON'T DO THIS
- ❌ Don't create duplicate flight numbers
- ❌ Don't use 12-hour time format
- ❌ Don't forget to set available seats
- ❌ Don't delete flights with active bookings without notice
- ❌ Don't use special characters in flight numbers
- ❌ Don't exceed seat capacity for aircraft type

---

## 🔍 View All Flights

### Quick Stats
- **Total Flights**: Shows count of all flights in system
- **Occupancy**: Percentage of seats booked
- **Available Seats**: Remaining bookable seats

### Filter/Search
- (Future feature: currently view only, no filtering)

---

## ⚠️ Warnings & Precautions

### Before Deleting a Flight
- Check number of bookings for that flight
- Consider notifying customers
- Verify no future bookings scheduled
- Backup flight data if needed

### If You Make a Mistake
- **Added wrong flight**: Delete it immediately
- **Wrong deletion**: Flight is permanently gone (no undo)
- **Want to recover**: Contact database administrator

---

## 📞 Troubleshooting

### "Flight number already exists" Error
- **Problem**: You entered a flight number that's already in database
- **Solution**: Use a different flight number
- **Check**: Scroll through list to ensure unique number

### "Please fill in all required fields" Error
- **Problem**: One or more fields were left blank
- **Solution**: Ensure all 7 fields are completed
- **Required fields**: All are mandatory

### "Error adding flight" Message
- **Problem**: Database connection issue or invalid data
- **Solution**: Check your data format and try again
- **Contact**: Admin if issue persists

### Flight Not Appearing After Add
- **Problem**: Page didn't refresh or data wasn't committed
- **Solution**: Click back to flights list, flight should appear
- **Try**: Refresh page with F5

### Delete Button Not Working
- **Problem**: JavaScript confirmation dialog issue
- **Solution**: Try again, ensure you click "OK" on confirmation
- **Try**: Use different browser if persistent

---

## 📅 Regular Maintenance

### Daily Tasks
- [ ] Review new flight bookings
- [ ] Check flight occupancy rates
- [ ] Monitor customer support messages

### Weekly Tasks
- [ ] Review and update flight schedules
- [ ] Add seasonal flights if needed
- [ ] Remove obsolete/past flights
- [ ] Check booking confirmations

### Monthly Tasks
- [ ] Analyze flight performance
- [ ] Update pricing based on demand
- [ ] Plan new routes
- [ ] Review customer feedback

---

## 🚀 Future Enhancements

Coming soon:
- [ ] Edit flight details (update after creation)
- [ ] Bulk import flights (CSV upload)
- [ ] Flight status updates (delayed, cancelled, on-time)
- [ ] Seat map visualization
- [ ] Customer notifications on deletion
- [ ] Recurring flights (schedules)

---

Need help? Check the admin dashboard or contact support.
