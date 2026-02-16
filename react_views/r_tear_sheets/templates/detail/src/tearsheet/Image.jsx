// Same frame size as edit view so image displays identically
const IMAGE_FRAME_WIDTH = 816;
const IMAGE_FRAME_HEIGHT = 400;

export default function Image({ img, imageTransform }) {
	const scale = imageTransform?.image_scale != null ? Math.max(1, Number(imageTransform.image_scale)) : 1;
	const offsetX = imageTransform?.image_offset_x != null ? Number(imageTransform.image_offset_x) : 0;
	const offsetY = imageTransform?.image_offset_y != null ? Number(imageTransform.image_offset_y) : 0;

	if (!img) return null;

	return (
		<div
			style={{
				width: IMAGE_FRAME_WIDTH,
				height: IMAGE_FRAME_HEIGHT,
				overflow: 'hidden',
				position: 'relative',
			}}
		>
			<div
				style={{
					position: 'absolute',
					left: '50%',
					top: '50%',
					width: '100%',
					height: '100%',
					backgroundImage: `url(${img})`,
					backgroundSize: 'cover',
					backgroundPosition: 'center',
					transformOrigin: 'center',
					transform: `translate(-50%, -50%) translate(${offsetX}px, ${offsetY}px) scale(${scale})`,
				}}
			/>
		</div>
	);
}
