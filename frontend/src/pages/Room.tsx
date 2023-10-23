import { Add, Circle } from '@mui/icons-material'
import { motion } from 'framer-motion'
import { useRef, useState } from 'react'
import { useNavigate } from 'react-router'
import CodeEditor from '../components/CollaborationRoom/CodeEditor'
import ConfirmationBox from '../components/CollaborationRoom/ConfirmationBox.tsx'
import QuestionDescription from '../components/CollaborationRoom/QuestionDescription.tsx'
import { useMatch } from '../stores/matchingStore.ts'
import { useUser } from '../stores/userStore.ts'
import '../styles/Room.css'

export const Room = () => {
    const [showConfirmation, setShowConfirmation] = useState(false)
    const navigate = useNavigate()
    const constraintsRef = useRef(null)
    const { data: match } = useMatch()
    const { data: matchedUser } = useUser(match?.user_id)

    const handleExit = () => {
        setTimeout(() => {
            navigate('/questions')
        }, 2000) // 2000 milliseconds (2 seconds) delay
    }

    return (
        <div>
            <motion.div ref={constraintsRef}>
                <motion.div
                    className='chatbox'
                    style={{ display: 'flex' }}
                    drag='x'
                    dragElastic={false}
                    dragMomentum={false}
                    dragConstraints={constraintsRef}
                >
                    <div
                        style={{
                            display: 'flex',
                            justifyContent: 'flex-end',
                            alignItems: 'center',
                            width: '100%',
                        }}
                    >
                        <Add sx={{ marginRight: 'auto' }} />
                        <Circle sx={{ alignSelf: 'right', color: '#00b8a2', fontSize: '10px' }} />
                        <h3 style={{ color: 'white', margin: '12px' }}>{matchedUser!.username}</h3>
                    </div>
                </motion.div>
            </motion.div>

            {showConfirmation && (
                <ConfirmationBox onClose={() => setShowConfirmation(false)} onExit={handleExit} />
            )}
            <nav className='nav' style={{ padding: '8px 20px' }}>
                <h2
                    style={{
                        margin: '0 0 0 2rem',
                        padding: '0',
                        fontWeight: '500',
                        fontSize: '2rem',
                    }}
                >
                    PeerPrep
                </h2>
                <button
                    style={{ backgroundColor: '#fe375f', width: '200px', margin: '0' }}
                    onClick={() => setShowConfirmation(true)}
                >
                    Exit Room
                </button>
            </nav>
            <div className='split-container' style={{ padding: '20px' }}>
                <div className='pane' style={{ backgroundColor: '#303030', marginRight: '10px' }}>
                    <QuestionDescription />
                </div>
                <div className='pane' style={{ backgroundColor: '#303030', marginLeft: '10px' }}>
                    <CodeEditor />
                </div>
            </div>
        </div>
    )
}

export default Room
