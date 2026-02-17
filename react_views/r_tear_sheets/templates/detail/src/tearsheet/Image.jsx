// Same frame size as edit view so image displays identically (1500×1200, scaled to fit column)
const IMAGE_FRAME_WIDTH = 1500;
const IMAGE_FRAME_HEIGHT = 1200;
const COLUMN_WIDTH = 816;
const DISPLAY_SCALE = COLUMN_WIDTH / IMAGE_FRAME_WIDTH;
const DISPLAY_HEIGHT = Math.round(IMAGE_FRAME_HEIGHT * DISPLAY_SCALE);

export default function Image({ img, imageTransform }) {
	const scale = imageTransform?.image_scale != null ? Math.max(1, Number(imageTransform.image_scale)) : 1;
	const offsetX = imageTransform?.image_offset_x != null ? Number(imageTransform.image_offset_x) : 0;
	const offsetY = imageTransform?.image_offset_y != null ? Number(imageTransform.image_offset_y) : 0;

	if (!img) return null;

	return (
		<div style={{ maxWidth: COLUMN_WIDTH }}>
			<div
				style={{
					width: COLUMN_WIDTH,
					height: DISPLAY_HEIGHT,
					overflow: 'hidden',
					position: 'relative',
				}}
			>
				<div
					style={{
						position: 'absolute',
						left: 0,
						top: 0,
						width: IMAGE_FRAME_WIDTH,
						height: IMAGE_FRAME_HEIGHT,
						transform: `scale(${DISPLAY_SCALE})`,
						transformOrigin: '0 0',
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
			</div>
		</div>
	);
}
