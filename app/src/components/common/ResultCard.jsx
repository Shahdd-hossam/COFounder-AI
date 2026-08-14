function ResultCard({ title, children }) {
  return (
    <section className="result-card">
      <h2>{title}</h2>
      {children}
    </section>
  );
}

export default ResultCard;
