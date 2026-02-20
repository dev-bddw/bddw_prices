// Same frame size as detail view so PDF matches (1500×1200, scaled to fit column)
import PaneTree from './PaneTree';

const IMAGE_FRAME_WIDTH = 1500;
const IMAGE_FRAME_HEIGHT = 1200;
const COLUMN_WIDTH = 816;
const DISPLAY_SCALE = COLUMN_WIDTH / IMAGE_FRAME_WIDTH;
const DISPLAY_HEIGHT = Math.round(IMAGE_FRAME_HEIGHT * DISPLAY_SCALE);

export default function Image({ img, sdata, effectiveLayout }) {
	const hasPaneLayout = sdata?.pane_layout != null;
	const gutterWidth = sdata?.image_gutter_width ?? 8;

	// Multi-pane: render PaneTree read-only
	if (hasPaneLayout && effectiveLayout) {
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
						<PaneTree
							layout={effectiveLayout}
							path={[]}
							logicalWidth={IMAGE_FRAME_WIDTH}
							logicalHeight={IMAGE_FRAME_HEIGHT}
							gutterWidth={gutterWidth}
							displayScale={DISPLAY_SCALE}
						/>
					</div>
				</div>
			</div>
		);
	}

	// Legacy single-pane
	const scale = sdata?.image_scale != null ? Math.max(1, Number(sdata.image_scale)) : 1;
	const offsetX = sdata?.image_offset_x != null ? Number(sdata.image_offset_x) : 0;
	const offsetY = sdata?.image_offset_y != null ? Number(sdata.image_offset_y) : 0;

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
