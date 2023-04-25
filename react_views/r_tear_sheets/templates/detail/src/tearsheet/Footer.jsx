export default function Footer() {

	const current_year = new Date().getFullYear()

	return(
		<div style={{'font-size': '9px', 'letter-spacing': '2px','left':'90px','top': '1065px', 'position': 'absolute'}} className='text-gray-300'>
			BDDW - 5 CROSBY STREET NEW YORK NY 10013 - T 212 625 1230 - INFO@BDDW.COM - WWW.BDDW.COM - {current_year}
		</div>
	)
}
