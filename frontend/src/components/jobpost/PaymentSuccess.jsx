import { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import axios from "axios";

const PaymentSuccess = () => {
  const [searchParams] = useSearchParams();
  const txRef = searchParams.get("tx_ref");
  const [status, setStatus] = useState("verifying");
  const navigate = useNavigate();

  useEffect(() => {
    if (txRef) {
      verifyPayment(txRef);
    }
    // eslint-disable-next-line
  }, [txRef]);

  const verifyPayment = async (txRef) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/verify_payment/?tx_ref=${txRef}`);
      if (response.data.message === "Payment verified successfully!") {
        setStatus("success");
        // Redirect to job list after 3 seconds
        setTimeout(() => {
          navigate("/jobs");
        }, 3000);
      } else {
        setStatus("error");
      }
    } catch (error) {
      setStatus("error");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "3rem" }}>
      {status === "verifying" && <h1>Verifying your payment...</h1>}
      {status === "success" && (
        <>
          <h1>Payment verified successfully!</h1>
          <p>Your job post is now live. You will be redirected to job listings shortly.</p>
        </>
      )}
      {status === "error" && (
        <>
          <h1>Payment verification failed.</h1>
          <p>There was an error processing your payment. Please contact support if you were charged.</p>
        </>
      )}
    </div>
  );
};

export default PaymentSuccess;
