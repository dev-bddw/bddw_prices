export default function Footer() {

	const current_year = new Date().getFullYear()

	return(
		<div style={{'font-size': '10px', 'letter-spacing': '2px','left':'180px','top': '1355px', 'position': 'absolute'}} className='text-gray-400'>
			BDDW - 5 CROSBY STREET NEW YORK NY 10013 - T 212 625 1230 - INFO@BDDW.COM - WWW.BDDW.COM - {current_year}
		</div>
	)
}
