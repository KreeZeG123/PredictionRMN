export default function RightPane() {
  return (
    <div>
      <h2>Right Pane</h2>
      <button onClick={() => (alert('minimize right'))}>
        Envoyer au Left
      </button>
    </div>
  );
}
