import PageShell from "../components/common/PageShell";
import SWOTForm from "../components/swot/SWOTForm";

function SWOTAnalysis() {
  return (
    <PageShell
      title="SWOT Analysis Builder"
      subtitle="Map strategic strengths and risks to improve execution confidence."
    >
      <SWOTForm />
    </PageShell>
  );
}

export default SWOTAnalysis;
