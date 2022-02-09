import { useState, createContext } from "react";

export const ToolTipContext = createContext({
  data: {},
  updateTTData: () => {},
});
