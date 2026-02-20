export default function PaneLeaf({ leaf, logicalWidth, logicalHeight }) {
  const scale = leaf?.image_scale != null ? Math.max(1, Number(leaf.image_scale)) : 1;
  const offsetX = leaf?.image_offset_x != null ? Number(leaf.image_offset_x) : 0;
  const offsetY = leaf?.image_offset_y != null ? Number(leaf.image_offset_y) : 0;
  const imageUrl = leaf?.imageUrl ?? null;

  return (
    <div
      style={{
        width: logicalWidth,
        height: logicalHeight,
        overflow: 'hidden',
        position: 'relative',
      }}
    >
      {imageUrl ? (
        <div
          style={{
            position: 'absolute',
            left: '50%',
            top: '50%',
            width: '100%',
            height: '100%',
            backgroundImage: `url(${imageUrl})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            transformOrigin: 'center',
            transform: `translate(-50%, -50%) translate(${offsetX}px, ${offsetY}px) scale(${scale})`,
          }}
        />
      ) : (
        <div style={{ width: '100%', height: '100%', background: '#e5e7eb' }} />
      )}
    </div>
  );
}
