CREATE TABLE Inventory (
    EntryID INT IDENTITY(1,1) PRIMARY KEY,
    Title NVARCHAR(255) NOT NULL,
    Author NVARCHAR(255) NOT NULL,
    Genre NVARCHAR(100),
    PublicationDate DATE,
    ISBN NVARCHAR(20)
);
