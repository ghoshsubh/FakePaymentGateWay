document.getElementById('paymentForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    // Get current date and time
    const currentDate = new Date().toISOString().split('T')[0]; // YYYY-MM-DD format
    const currentTime = new Date().toLocaleTimeString(); // Local time format

    const transaction = {
        card_number: document.getElementById('cardNumber').value,
        cvv: document.getElementById('cvv').value,
        card_holder_name: document.getElementById('cardHolderName').value,
        expire_date: document.getElementById('expireDate').value,
        amount: parseFloat(document.getElementById('amount').value),
        date: currentDate, // Set to current date
        time: currentTime // Set to current time
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/AddTransactions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(transaction)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Create the success message
        const responseMessage = `Transaction successful with the following details:\nTransaction ID: ${data.payment_id}\nAmount: $${transaction.amount.toFixed(2)}\nDate: ${currentDate}\nTime: ${currentTime}`;
        
        // Set the text for the anchor tag and make it visible
        const responseElement = document.getElementById('responseMessage');
        //responseElement.href = `http://127.0.0.1:5000/transaction/${data.payment_id}`; // Link to the new endpoint
        
        //responseElement.innerText = "Payment Successfull\n See Payment Details"; // Set the link text
        responseElement.innerHTML = `Payment Successful!<br><br><a href="http://127.0.0.1:5000/transaction/${data.payment_id}" target="_blank">See Details</a>`;

        responseElement.style.display = 'inline'; // Make the link visible

        // Clear the input fields
        this.reset(); // Resets the form fields to their initial values

    } catch (error) {
        const responseElement = document.getElementById('responseMessage');
        responseElement.innerText = `Error: ${error.message}`;
        responseElement.style.display = 'inline'; // Make the error message visible
    }
});
