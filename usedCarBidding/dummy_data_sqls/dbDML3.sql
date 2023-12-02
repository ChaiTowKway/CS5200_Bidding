-- Assuming 'User' table is already filled

-- Inserting dummy data into 'Car'
INSERT INTO Car (Car_ID, Body_Style, Exterior_Color, Transmission, Mileage, Engine, Title_Status, Make, Model, Year, Drivetrain, Location, Current_Status, Seller_ID)
VALUES
('JTDT4RCE7LJ025456', 'Sedan', 'Red', 'Automatic', 10000, 'V6', 'Clean', 'Toyota', 'Corolla', 2020, 'FWD', 'New York', 'Available', 3),
('C2', 'Coupe', 'Blue', 'Manual', 5000, 'V8', 'Clean', 'Ford', 'Mustang', 1965, 'RWD', 'Los Angeles', 'Available', 4);

-- Inserting dummy data into 'Shipping'
INSERT INTO Shipping (Shipping_ID, Transport_Tracking_Number, Shipping_Method, Delivered_Date, Temp_hold, Shipping_Status)
VALUES
(1, 'TTN123', 'UPS', '2023-04-01 00:00:00', 'No', 'Delivered'),
(2, 'TTN456', 'FedEx', '2023-04-15 00:00:00', 'No', 'Delivered');

-- Inserting dummy data into 'Auction'
INSERT INTO Auction (Auction_ID, Start_Time, Car_ID, Minimum_Price, Ending_Time, Additional_Info, Winner_id, Minimum_Deposit, Auction_Hold, Auction_Status, is_verified, Payment_ID, Shipping_ID, Edit_time, Withdrawn)
VALUES
(1, '2023-03-01 00:00:00', 'JTDT4RCE7LJ025456', 10000.00, '2023-03-10 00:00:00', 'Info about auction 1', 2, 500.00, 0, 'Open', 1, 100, 1, '2023-03-02 00:00:00', 'No'),
(2, '2023-03-15 00:00:00', 'C2', 20000.00, '2023-03-25 00:00:00', 'Info about auction 2', 1, 1000.00, 0, 'Open', 1, 101, 2, '2023-03-16 00:00:00', 'No');



-- Inserting dummy data into 'Bidding'
INSERT INTO Bidding (Bidding_ID, Auction_ID, Bidder_ID, Bidding_Price)
VALUES
(1, 1, 1, 15000.00),
(2, 2, 2, 25000.00);

-- Inserting dummy data into 'Comments'
INSERT INTO Comments (CommentID, CommenContent, create_at, create_by_user_ID, create_by_user_Name, auction_id)
VALUES
(1, 'Nice car!', '2023-03-01', 1, 'User One', 1),
(2, 'Good deal!', '2023-03-02', 2, 'User Two', 2);

-- Inserting dummy data into 'Reply'
INSERT INTO reply (Reply_ID, ReplyContent, create_at, create_by_user_ID, create_by_user_Name, CommentID)
VALUES
(1, 'Thank you!', '2023-03-03', 2, 'User Two', 1),
(2, 'I agree!', '2023-03-04', 1, 'User One', 2);
