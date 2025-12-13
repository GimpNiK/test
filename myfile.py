predictions_round = np.round(predictions)

ans = y_test - predictions_round
print(ans)
counter = 0
for i in range(len(ans)):
    if ans[i] == 0:
        counter += 1
accuaracy = counter / len(ans)