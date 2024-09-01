type Temp = Float

data Termostat = On | Off

-- data MDP = MDP a a

-- class State s where
--   (|||) :: s -> a -> Maybe [(s -> s, Float)]

-- instance State (MDP Temp Termo) where
--   16 ||| On = zip [0.9, 0.1, 0] [(\x -> x), (\x -> x+0.5), (\x -> x-0.5)]
-- --type ProbList = [(Float, (s -> s))]

-- condProbOn :: State s => s -> [Float] -> s
-- condProbOn s _ = s

goal = 22

class Action a where
  actionCost :: a -> Float

instance Action Termostat where
  actionCost On = 4
  actionCost Off = 1


type Iterations = Int
type Prob = Float

possibleActions :: Float -> [Termostat]
possibleActions t
   | t == goal = []
   | otherwise = [On, Off]

--probCond :: MDP s a => s -> a -> [(s, Float)]
probCond :: Temp -> Termostat -> [(Temp, Prob)]
probCond s a = zip (nextState s a) (probNextState s a)

nextState :: Temp -> Termostat -> [Prob]
nextState t On = [t, t+0.5, t+1, t-0.5]
nextState t Off = [t, t+0.5, t-0.5]

probNextState :: Temp -> Termostat -> [Temp]
probNextState t On
  | t == 16 = [0.3, 0.5, 0.2, 0]
  | t == 24.5 = [0.2, 0.7, 0, 0.1]
  | t == 25 = [0.2, 0, 0, 0.1]
  | t < 16 || t > 25 = []
  | otherwise = [0.2, 0.5, 0.2, 0.1]
probNextState t Off
  | t == 16 = [0.9, 0.1, 0]
  | t == 25 = [0.3, 0, 0.7]
  | t < 16 || t > 25 = []
  | otherwise = [0.2, 0.1, 0.7]

--valueIteration t 0 = 0
valueIteration :: Temp -> Iterations -> Float
valueIteration t 0 = 0
valueIteration t i = minimum $ prevValue <$> possibleActions t
  where
    prevValue a =  foldr (\(s', p) z -> z + p * valueIteration s' i-1) (actionCost a) (probCond t a)

