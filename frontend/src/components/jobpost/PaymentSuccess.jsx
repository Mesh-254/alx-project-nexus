import { useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import axios from "axios";

const PaymentSuccess = () => {
  const [searchParams] = useSearchParams();
  const txRef = searchParams.get("tx_ref");

  useEffect(() => {
    if (txRef) {
      verifyPayment(txRef);
    }
  }, [txRef]);

  const verifyPayment = async (txRef) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/verify_payment/?tx_ref=${txRef}`);
      console.log(response.data);
      alert("Payment verified successfully!");
    } catch (error) {
      console.error("Payment verification failed:", error);
      alert("Payment verification failed. Please try again.");
    }
  };

  return (
    <div>
      <h1>Payment Verification in Progress...</h1>
    </div>
  );
};

export default PaymentSuccess;
