export default function LeftPane() {
  return (
    <div>
      <h2>Left Pane</h2>
      <button onClick={() => (alert('minimize left'))}>
        Répondre au Right
      </button>
    </div>
  );
}
